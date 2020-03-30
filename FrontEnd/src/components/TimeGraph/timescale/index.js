/*
DVAF -  offers the security-research community with up-to-date information
        about vulnerability trends, types, etc.

Copyright (C) 2019-2020
Nikolaos Alexopoulos <alexopoulos@tk.tu-darmstadt.de>,
Lukas Hildebrand <lukas.hildebrand@stud.tu-darmstadt.de>,
Jörn Schöndube <joe.sch@protonmail.com>,
Tim Lange <tim.lange@stud.tu-darmstadt.de>,
Moritz Wirth <mw@flanga.io>,
Paul-David Zürcher <mail@pauldavidzuercher.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.
*/
import React, { Component } from 'react';
import uniqueId from 'react-html-id';
import PropTypes from 'prop-types';
import './timescale.scss';
import GraphSwitch from '../../GraphSwitch';

/**
 * Enum for the different timesteps
 */
export const timeShown = Object.freeze({
  year: 'year',
  month: 'month',
  day: 'day',
});

/**
 * Daterange and Timestep Input for TimeGraphs
 */
class Timescale extends Component {
  constructor(props) {
    super(props);

    // maps timeShown to string index for cutting timestamps
    this.timeToIndex = Object.freeze({
      year: 4,
      month: 7,
      day: 10,
    });
    // maps timeShown to html input type
    this.timeToInput = Object.freeze({
      year: 'number',
      month: 'month',
      day: 'date',
    });

    // Calculates the default start dates using the current date
    const today = new Date();
    const dd = String(today.getDate()).padStart(2, '0');
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const yyyy = today.getFullYear();
    const twentyYearsBefore = new Date(today);
    twentyYearsBefore.setFullYear(twentyYearsBefore.getFullYear() - 20);
    const yearBefore = new Date(today);
    yearBefore.setFullYear(yearBefore.getFullYear() - 1);
    const monthBefore = new Date(today);
    monthBefore.setMonth(monthBefore.getMonth() - 1);

    this.state = {
      show: this.props.defaultShown,
      year: {
        start: `${twentyYearsBefore.getFullYear()}`,
        end: yyyy,
      },
      month: {
        start: `${yearBefore.getFullYear()}-${String(yearBefore.getMonth() + 1).padStart(2, '0')}`,
        end: `${yyyy}-${mm}`,
      },
      day: {
        start: `${monthBefore.getFullYear()}-${String(monthBefore.getMonth() + 1).padStart(2, '0')}-${String(
          monthBefore.getDate(),
        ).padStart(2, '0')}`,
        end: `${yyyy}-${mm}-${dd}`,
      },
      min: '1980-1-1',
      max: `${yyyy}-${mm}-${dd}`,
    };

    this.timeout = null;
    this.handleInputChange = this.handleInputChange.bind(this);
    this.changeShownTimeframe = this.changeShownTimeframe.bind(this);

    uniqueId.enableUniqueIds(this);
  }

  componentDidMount() {
    this.props.changeTimeframe(this.formatDate());
  }

  componentDidUpdate(prevProps) {
    if (this.props.chartUrl === prevProps.chartUrl) return;

    this.props.changeTimeframe(this.formatDate());
  }

  /**
   * Changes the values according to the clicked bar in the TimeGraph
   * @param {string} dateString
   */
  onBarClick(dateString) {
    // fix for firefox not being able to interpret "Oct 2018"
    let startDate = new Date(this.state.show === timeShown.month ? `01 ${dateString}` : dateString);
    let endDate;

    if (this.state.show === timeShown.year) {
      startDate = new Date(startDate.getFullYear(), 0, 1);
      endDate = new Date(startDate.getFullYear() + 1, 0, 0);
      this.setInput([timeShown.month, 'start'], `${startDate.getFullYear()}-${String(startDate.getMonth() + 1).padStart(2, '0')}`);
      this.setInput([timeShown.month, 'end'], `${endDate.getFullYear()}-${String(endDate.getMonth() + 1).padStart(2, '0')}`);
      this.setState({ show: timeShown.month }, () => this.props.changeShownTimeframe(this.state.show, this.formatDate()));
    } else if (this.state.show === timeShown.month) {
      startDate = new Date(startDate.getFullYear(), startDate.getMonth(), 1);
      endDate = new Date(startDate.getFullYear(), startDate.getMonth() + 1, 0);
      this.setInput(
        [timeShown.day, 'start'],
        `${startDate.getFullYear()}-${String(startDate.getMonth() + 1).padStart(2, '0')}-${String(startDate.getDate()).padStart(2, '0')}`,
      );
      this.setInput(
        [timeShown.day, 'end'],
        `${endDate.getFullYear()}-${String(endDate.getMonth() + 1).padStart(2, '0')}-${String(endDate.getDate()).padStart(2, '0')}`,
      );
      this.setState({ show: timeShown.day }, () => this.props.changeShownTimeframe(this.state.show, this.formatDate()));
    }
    // day click does nothing atm
  }

  /**
   * Sets the input
   * @param {array} name tupel of timestep and (start|end)
   * @param {string} value date
   */
  setInput(name, value) {
    this.setState(
      // update input
      prev => {
        const newState = { ...prev };
        newState[name[0]][name[1]] = value;
        return newState;
      },
      // send valid input to parent after 250ms
      () => {
        this.timeout = setTimeout(() => {
          if (this.validateInput(value)) this.props.changeTimeframe(this.formatDate());
        }, 250);
      },
    );
  }

  /**
   * Updates the inputs
   * @param {*} e event from input change
   */
  handleInputChange(e) {
    clearTimeout(this.timeout);
    const name = e.target.name.split('_');
    const { value } = e.target;
    this.setInput(name, value);
  }

  /**
   * Checks if the dateString is in a valid format
   * @param  {string} dateString
   * @returns {boolean} dateString is valid
   */
  validateInput(dateString) {
    const date = Date.parse(dateString);
    // string got the right length && is a number && date between min and max && start < end
    return (
      dateString.length === this.timeToIndex[this.state.show] &&
      Number.isFinite(date) &&
      Date.parse(this.state.min) <= date <= Date.parse(this.state.max) &&
      Date.parse(this.state[this.state.show].start) <= Date.parse(this.state[this.state.show].end)
    );
  }

  /**
   * Translates the date input to the dd-mm-yyyy format
   * @returns {object} start and end date in dd-mm-yyyy ready for api usage
   */
  formatDate() {
    const ymdStartDate = this.state[this.state.show].start;
    const ymdEndDate = this.state[this.state.show].end;

    const startDate = new Date(ymdStartDate.toString());
    let endDate = new Date(ymdEndDate.toString());

    if (this.state.show === timeShown.year) {
      // Adds last day of year
      endDate = new Date(endDate.getFullYear() + 1, 0, 0);
    } else if (this.state.show === timeShown.month) {
      // Adds last day of month
      endDate = new Date(endDate.getFullYear(), endDate.getMonth() + 1, 0);
    }

    const dmyStartDate = `${String(startDate.getDate()).padStart(2, '0')}-${String(startDate.getMonth() + 1).padStart(
      2,
      '0',
    )}-${startDate.getFullYear()}`;
    const dmyEndDate = `${String(endDate.getDate()).padStart(2, '0')}-${String(endDate.getMonth() + 1).padStart(
      2,
      '0',
    )}-${endDate.getFullYear()}`;

    return { dmyStartDate, dmyEndDate };
  }

  /**
   * Updates the selected time step
   * @param {*} e event from button click
   */
  changeShownTimeframe(e) {
    const text = e.target.innerText;

    this.setState({ show: timeShown[text] }, () => {
      // pass state to parent
      this.props.changeShownTimeframe(this.state.show, this.formatDate());
    });
  }

  render() {
    return (
      <div className="timescale">
        {this.props.expandable && <GraphSwitch defaultChecked={false} onChange={e => this.props.changeView(e, this.formatDate())} />}
        <div className={`${this.state.show} form-row align-items-center justify-content-center`}>
          <div>
            from
            <input
              type={this.timeToInput[this.state.show]}
              name={`${this.state.show}_start`}
              value={this.state[this.state.show].start}
              onChange={e => this.handleInputChange(e)}
              min={this.state.min.substr(0, this.timeToIndex[this.state.show])}
              max={this.state[this.state.show].end}
              className="mx-2 form-control form-control-sm d-inline"
            />
          </div>
          <div>
            to
            <input
              type={this.timeToInput[this.state.show]}
              name={`${this.state.show}_end`}
              value={this.state[this.state.show].end}
              onChange={e => this.handleInputChange(e)}
              min={this.state[this.state.show].start}
              max={this.state.max.substr(0, this.timeToIndex[this.state.show])}
              className="mx-2 form-control form-control-sm d-inline"
            />
          </div>
        </div>
        <div className="btn-group btn-group-sm mt-1" role="group">
          <button
            type="button"
            onClick={e => this.changeShownTimeframe(e)}
            className={this.state.show === timeShown.day ? 'btn btn-secondary' : 'btn btn-outline-secondary'}
          >
            day
          </button>
          <button
            type="button"
            onClick={e => this.changeShownTimeframe(e)}
            className={this.state.show === timeShown.month ? 'btn btn-secondary' : 'btn btn-outline-secondary'}
          >
            month
          </button>
          <button
            type="button"
            onClick={e => this.changeShownTimeframe(e)}
            className={this.state.show === timeShown.year ? 'btn btn-secondary' : 'btn btn-outline-secondary'}
          >
            year
          </button>
        </div>
      </div>
    );
  }
}

Timescale.propTypes = {
  /** Default shown timestep */
  defaultShown: PropTypes.string.isRequired,
  /** Function called when the daterange changes */
  changeTimeframe: PropTypes.func.isRequired,
  /** Function called when the daterange and timestep changes */
  changeShownTimeframe: PropTypes.func.isRequired,
  /** Function called on switch of view mode (graph/table view) */
  changeView: PropTypes.func.isRequired,
  /** API url (used to track a change of the package) */
  chartUrl: PropTypes.string.isRequired,
  /** If true, the GraphSwitch is shown */
  expandable: PropTypes.bool.isRequired,
};

export default Timescale;
