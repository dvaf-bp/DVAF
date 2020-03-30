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
import PropTypes from 'prop-types';
import './timescale.scss';
import { BASE_URL } from '../../constants';

export const timeShown = Object.freeze({
  year: 'year',
  month: 'month',
  day: 'day',
});

class Timescale extends Component {
  constructor(props) {
    super(props);

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
      show: this.props.show,
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
      saved_data: {
        year: {
          labels: [],
          data: [],
          expanded: [],
        },
        month: {
          labels: [],
          data: [],
          expanded: [],
        },
        day: {
          labels: [],
          data: [],
          expanded: [],
        },
      },
    };

    this.timeout = null;
    this.handleChange = this.handleChange.bind(this);
  }

  componentDidMount() {
    this.getData();
  }

  componentDidUpdate(prevProps) {
    if (this.props.url === prevProps.url) return;

    this.getData();
  }

  getData() {
    const { startDate, endDate } = this.formatDate(this.state[this.state.show].start, this.state[this.state.show].end);
    const url = `${this.props.url}/${startDate}/${endDate}/${this.state.show}`;
    fetch(BASE_URL + url)
      .then(response => response.json())
      .then(data => {
        let res;
        let labels;
        let expanded = [];

        if (this.props.mode === 'package') {
          res = [data.closed_cve_count, data.open_cve_count];
          labels = data.dates;
          expanded = this.props.expanded ? data.closed_cves.map((e, i) => e.concat(data.open_cves[i])) : [];
        } else {
          res = [this.props.expanded ? data.cves.map(e => e.length) : data.cves_count];
          labels = data.labels;
          expanded = data.cves;
        }
        labels = labels.map(e => {
          if (this.state.show === timeShown.year) return e.substr(12, 4);
          if (this.state.show === timeShown.month) return e.substr(8, 8);
          return e.substr(5, 11);
        });

        this.setState(
          prev => {
            const newState = { ...prev };
            newState.saved_data[prev.show].labels = labels;
            newState.saved_data[prev.show].data = res;
            newState.saved_data[prev.show].expanded = expanded;
            return newState;
          },
          () => {
            this.props.changeData(labels, res, expanded);
          },
        );
      })
      .catch(e => console.error(e));
  }

  formatDate(pStartDate, pEndDate) {
    let startDate = pStartDate;
    let endDate = pEndDate;

    if (this.state.show === timeShown.year) {
      startDate += '-01-01';
      endDate += '-12-31';
    } else if (this.state.show === timeShown.month) {
      startDate += '-01';
      endDate += '-31';
    }
    startDate = startDate
      .split('-')
      .reverse()
      .join('-');
    endDate = endDate
      .split('-')
      .reverse()
      .join('-');
    return { startDate, endDate };
  }

  validateInput(dateString) {
    const date = Date.parse(dateString);
    let len;

    if (this.state.show === timeShown.year) len = 4;
    else if (this.state.show === timeShown.month) len = 7;
    else len = 10;

    return dateString.length === len && Number.isFinite(date) && Date.parse(this.state.min) <= date <= Date.parse(this.state.max);
  }

  handleChange(e) {
    clearTimeout(this.timeout);
    const name = e.target.name.split('_');
    const { value } = e.target;

    this.setState(
      prev => {
        const newState = { ...prev };
        newState[name[0]][name[1]] = value;
        return newState;
      },
      () => {
        this.timeout = setTimeout(() => {
          if (this.validateInput(value)) this.getData();
        }, 250);
      },
    );
  }

  updateShow(e) {
    this.setState({ show: timeShown[e.target.innerText] }, () => {
      if (this.state.saved_data[this.state.show].labels.length === 0) this.getData();
      else
        this.props.changeData(
          this.state.saved_data[this.state.show].labels,
          this.state.saved_data[this.state.show].data,
          this.state.saved_data[this.state.show].expanded,
        );
    });
  }

  render() {
    const year = (
      <div className="year form-row align-items-center justify-content-center">
        <div>
          from
          <input
            type="number"
            name="year_start"
            value={this.state.year.start}
            onChange={this.handleChange}
            min={this.state.min.substr(0, 4)}
            max={this.state.year.end}
            className="mx-2 form-control form-control-sm d-inline"
          />
        </div>
        <div>
          to
          <input
            type="number"
            name="year_end"
            value={this.state.year.end}
            onChange={this.handleChange}
            min={this.state.year.start}
            max={this.state.max.substr(0, 4)}
            className="mx-2 form-control form-control-sm d-inline"
          />
        </div>
      </div>
    );
    const month = (
      <div className="month form-row align-items-center justify-content-center">
        <div>
          from
          <input
            type="month"
            name="month_start"
            value={this.state.month.start}
            onChange={this.handleChange}
            min={this.state.min.substr(0, 7)}
            max={this.state.month.end}
            className="mx-2 form-control form-control-sm d-inline"
          />
        </div>
        <div>
          to
          <input
            type="month"
            name="month_end"
            value={this.state.month.end}
            onChange={this.handleChange}
            min={this.state.month.start}
            max={this.state.max.substr(0, 7)}
            className="mx-2 form-control form-control-sm d-inline"
          />
        </div>
      </div>
    );
    const day = (
      <div className="day form-row align-items-center justify-content-center">
        <div>
          from
          <input
            type="date"
            name="day_start"
            value={this.state.day.start}
            onChange={this.handleChange}
            min={this.state.min}
            max={this.state.day.end}
            className="mx-2 form-control form-control-sm d-inline"
          />
        </div>
        <div>
          to
          <input
            type="date"
            name="day_end"
            value={this.state.day.end}
            onChange={this.handleChange}
            min={this.state.day.start}
            max={this.state.max}
            className="mx-2 form-control form-control-sm d-inline"
          />
        </div>
      </div>
    );

    let inputs;
    if (this.state.show === 'day') {
      inputs = day;
    } else if (this.state.show === 'month') {
      inputs = month;
    } else {
      inputs = year;
    }

    return (
      <div className="timescale">
        {inputs}
        <div className="btn-group btn-group-sm mt-1" role="group">
          <button
            type="button"
            onClick={e => this.updateShow(e)}
            className={this.state.show === 'day' ? 'btn btn-secondary' : 'btn btn-outline-secondary'}
          >
            day
          </button>
          <button
            type="button"
            onClick={e => this.updateShow(e)}
            className={this.state.show === 'month' ? 'btn btn-secondary' : 'btn btn-outline-secondary'}
          >
            month
          </button>
          <button
            type="button"
            onClick={e => this.updateShow(e)}
            className={this.state.show === 'year' ? 'btn btn-secondary' : 'btn btn-outline-secondary'}
          >
            year
          </button>
        </div>
      </div>
    );
  }
}

Timescale.propTypes = {
  changeData: PropTypes.func.isRequired,
  url: PropTypes.string.isRequired,
  expanded: PropTypes.bool,
  show: PropTypes.node.isRequired,
  mode: PropTypes.string.isRequired,
};

Timescale.defaultProps = {
  expanded: false,
};

export default Timescale;
