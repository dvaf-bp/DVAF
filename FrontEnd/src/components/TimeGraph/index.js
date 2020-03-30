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
import Bar from 'react-chartjs-2';
import 'chartjs-plugin-trendline';
import PropTypes from 'prop-types';
import Spinner from 'react-bootstrap/Spinner';
import mergeRefs from 'react-merge-refs';
import Timescale, { timeShown } from './timescale';
import CVETable from '../CVETable';
import Accordion from '../Accordion';
import AccordionHeader from '../Accordion/Header';
import AccordionContainer from '../Accordion/Container';
import AccordionContent from '../Accordion/Content';
import { BASE_URL } from '../../constants';

/**
 * Graph by time with changeable daterange and timestep
 */
class TimeGraph extends Component {
  constructor(props) {
    super(props);

    this.changeView = this.changeView.bind(this);
    this.changeShownTimeframe = this.changeShownTimeframe.bind(this);
    this.changeTimeframe = this.changeTimeframe.bind(this);
    this.onBarClick = this.onBarClick.bind(this);
    this.toggleCursor = this.toggleCursor.bind(this);

    this.options = this.props.mode.getOptions(this.props.xLabel, this.props.yLabel, this.onBarClick, this.toggleCursor);

    this.state = {
      labels: [],
      datasets: this.props.mode.getDefaultDatasets(),
      table: [],
      show: this.props.show,
      dataShown: '',
      expanded: this.props.expandable && this.props.expanded,
    };

    this.chartRef = React.createRef();
    this.timescaleRef = React.createRef();
  }

  /**
   * Handles click on bar of graph
   * @param {*} e click event
   */
  onBarClick(e) {
    const elements = this.chartRef.current.chartInstance.chart.getElementAtEvent(e);
    if (elements.length === 0) return;

    // this is chartjs
    // eslint-disable-next-line
    this.timescaleRef.current.onBarClick(this.state.labels[elements[0]._index]);
  }

  /**
   * Handles hover on bar of graph. Changes cursor to pointer.
   * @param {*} e hover event
   */
  toggleCursor(e) {
    const elements = this.chartRef.current.chartInstance.chart.getElementAtEvent(e);
    this.chartRef.current.chartInstance.canvas.style.cursor =
      elements.length > 0 && this.state.show !== timeShown.day ? 'pointer' : 'default';
  }

  /**
   * Changes the view between table and graph view
   * @param {*} expanded If true, switch to table view
   * @param {array} dates tuple of datestrings
   */
  changeView(expanded, dates) {
    if (this.props.expandable) this.setState({ expanded }, () => this.changeTimeframe(dates));
  }

  /**
   * Changes the timestep and then reloads the data
   * @param {string} show timestep
   * @param {array} dates tuple of datestrings
   */
  changeShownTimeframe(show, dates) {
    this.setState({ show }, () => this.changeTimeframe(dates));
  }

  /**
   * Reloads the data
   * @param {array} dates tuple of datestrings
   */
  changeTimeframe(dates) {
    const { dmyStartDate, dmyEndDate } = dates;
    const url = `${this.state.expanded ? this.props.tableUrl : this.props.chartUrl}/${dmyStartDate}/${dmyEndDate}/${this.state.show}`;
    fetch(BASE_URL + url)
      .then(response => response.json())
      .then(data => {
        const retval = this.state.expanded ? this.props.mode.processTableData(data) : this.props.mode.processGraphData(data);
        let { labels } = retval;
        labels = labels.map(e => {
          if (this.state.show === timeShown.year) return e.substr(12, 4);
          if (this.state.show === timeShown.month) return e.substr(8, 8);
          return e.substr(5, 11);
        });

        if (this.state.expanded) {
          const { table } = retval;
          this.setState(prev => ({ labels, table, dataShown: prev.show }));
        } else {
          const { datasets } = retval;
          this.setState(prev => ({ labels, datasets, dataShown: prev.show }));
        }
      })
      .catch(e => console.error(e));
  }

  render() {
    return (
      <>
        <Timescale
          defaultShown={this.props.show}
          changeTimeframe={this.changeTimeframe}
          changeShownTimeframe={this.changeShownTimeframe}
          changeView={this.changeView}
          expandable={this.props.expandable}
          chartUrl={this.props.chartUrl}
          ref={this.timescaleRef}
        />
        {this.state.show !== this.state.dataShown && (
          <div className="d-flex justify-content-center align-items-center">
            <Spinner className="text-center my-4" as="span" animation="border" size="sm" role="status" aria-hidden="true" />
          </div>
        )}
        {!this.state.expanded ? (
          <div className="canvas-container" style={{ visibility: this.state.show !== this.state.dataShown ? 'hidden' : 'visible' }}>
            <Bar
              ref={mergeRefs([this.chartRef, this.props.forwardRef])}
              data={{ labels: this.state.labels, datasets: this.state.datasets }}
              options={this.options}
              type="bar"
            />
          </div>
        ) : (
          [
            this.state.table.length > 0 ? (
              <Accordion
                id="timeAccordion"
                className="my-4"
                style={{ visibility: this.state.show !== this.state.dataShown ? 'hidden' : 'visible' }}
              >
                {this.state.labels.map((label, i) => {
                  const lbl = label.replace(/\s/g, '');
                  if (!this.state.table || this.state.table[i].length === 0) return '';
                  return (
                    <AccordionContainer key={lbl}>
                      <AccordionHeader for={lbl}>{label}</AccordionHeader>

                      <AccordionContent for={lbl} parent="timeAccordion">
                        <CVETable cves={this.state.table[i]} />
                      </AccordionContent>
                    </AccordionContainer>
                  );
                })}
              </Accordion>
            ) : (
              <div className="d-flex justify-content-center align-items-center">
                <Spinner className="text-center my-4" as="span" animation="border" size="sm" role="status" aria-hidden="true" />
              </div>
            ),
          ]
        )}
      </>
    );
  }
}

TimeGraph.propTypes = {
  /** If true, the table view is shown by default */
  expanded: PropTypes.bool,
  /** If true, the Graph Switch is shown */
  expandable: PropTypes.bool,
  /** Label for the x-axis */
  xLabel: PropTypes.string,
  /** Label for the y-axis */
  yLabel: PropTypes.string,
  /** API URL for the graph data */
  chartUrl: PropTypes.string.isRequired,
  /** API URL for the table data */
  tableUrl: PropTypes.string,
  /** Reference for ChartComponent */
  forwardRef: PropTypes.oneOfType([PropTypes.func, PropTypes.shape({ current: PropTypes.any })]),
  /** Default shown timestep */
  show: PropTypes.string,
  /** Graph mode, provides functions to convert api response to graph data */
  mode: PropTypes.shape({
    processGraphData: PropTypes.func,
    processTableData: PropTypes.func,
    getOptions: PropTypes.func,
    getDefaultDatasets: PropTypes.func,
  }).isRequired,
};
TimeGraph.defaultProps = {
  expanded: false,
  xLabel: '',
  yLabel: '',
  forwardRef: null,
  show: timeShown.year,
  tableUrl: '',
  expandable: true,
};

export default TimeGraph;
