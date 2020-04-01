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
import Timescale, { timeShown } from './timescale';
import CVETable from '../CVETable';
import Accordion from '../Accordion';
import AccordionHeader from '../Accordion/Header';
import AccordionContainer from '../Accordion/Container';
import AccordionContent from '../Accordion/Content';

class TimeGraph extends Component {
  constructor(props) {
    super(props);

    this.options = {
      responsive: true,
      maintainAspectRatio: false,
      legend: {
        display: false,
      },
      tooltips: {
        mode: 'index',
        intersect: false,
      },
      scales: {
        xAxes: [
          {
            stacked: true,
            scaleLabel: {
              display: true,
              labelString: this.props.xLabel,
            },
          },
        ],
        yAxes: [
          {
            stacked: true,
            ticks: {
              beginAtZero: true,
            },
            scaleLabel: {
              display: true,
              labelString: this.props.yLabel,
            },
          },
        ],
      },
    };

    this.state = {
      chartData: {
        labels: [],
        datasets:
          this.props.mode === 'package'
            ? [
                {
                  trendlineLinear: {
                    style: '#2ecc71',
                    width: 2,
                  },
                  label: 'closed vulnerabilities',
                  data: [0],
                  backgroundColor: '#2ecc71',
                  borderColor: '#27ae60',
                  borderWidth: 2,
                },
                {
                  trendlineLinear: {
                    style: '#fc5c65',
                    width: 2,
                  },
                  label: 'open vulnerabilities',
                  data: [0],
                  backgroundColor: '#fc5c65',
                  borderColor: '#eb3b5a',
                  borderWidth: 2,
                },
              ]
            : [
                {
                  trendlineLinear: {
                    style: '#45aaf2',
                    width: 2,
                  },
                  label: 'vulnerabilities',
                  data: [0],
                  backgroundColor: '#fc5c65',
                  borderColor: '#eb3b5a',
                  borderWidth: 2,
                },
              ],
      },
      cvelist: [],
      expanded: this.props.expanded,
    };

    this.changeData = this.changeData.bind(this);
    this.changeView = this.changeView.bind(this);
  }

  changeData(labels, datas, expanded) {
    this.setState(prev => {
      const newState = { ...prev };
      newState.chartData.labels = labels;
      datas.forEach((data, i) => {
        newState.chartData.datasets[i].data = [...data];
      });
      newState.cvelist = expanded;
      return newState;
    });
  }

  changeView(expanded) {
    this.setState({ expanded });
  }

  render() {
    const { labels } = this.state.chartData;

    return (
      <>
        <Timescale
          mode={this.props.mode}
          show={this.props.show}
          expanded={this.state.expanded}
          changeData={this.changeData}
          changeView={this.changeView}
          chartUrl={this.props.chartUrl}
          tableUrl={this.props.tableUrl}
          expandable={this.props.expandable}
        />
        {!this.state.expanded ? (
          <div className="canvas-container">
            <Bar ref={this.props.forwardRef} data={this.state.chartData} options={this.options} type="bar" />
          </div>
        ) : (
          [
            this.state.cvelist.length > 0 ? (
              <Accordion id="timeAccordion" className="my-4">
                {labels.map((label, i) => {
                  const lbl = label.replace(/\s/g, '');
                  if (!this.state.cvelist || this.state.cvelist[i].length === 0) return '';
                  return (
                    <AccordionContainer key={lbl}>
                      <AccordionHeader for={lbl}>{label}</AccordionHeader>

                      <AccordionContent for={lbl} parent="timeAccordion">
                        <CVETable cves={this.state.cvelist[i]} />
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
  expanded: PropTypes.bool,
  xLabel: PropTypes.string,
  yLabel: PropTypes.string,
  chartUrl: PropTypes.string.isRequired,
  tableUrl: PropTypes.string,
  forwardRef: PropTypes.oneOfType([PropTypes.func, PropTypes.shape({ current: PropTypes.any })]),
  show: PropTypes.node,
  mode: PropTypes.string.isRequired,
  expandable: PropTypes.bool,
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
