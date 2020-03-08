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
import { Link } from 'react-router-dom';
import Bar from 'react-chartjs-2';
import 'chartjs-plugin-trendline';
import PropTypes from 'prop-types';
import Timescale, { timeShown } from '../timescale';

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
    };

    this.changeData = this.changeData.bind(this);
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

  render() {
    let ex = '';
    const { labels } = this.state.chartData;
    if (this.props.expanded)
      ex = (
        <div className="accordion my-4" id="accordionExample">
          {labels.map((label, i) => {
            const lbl = label.replace(/\s/g, '');
            if (this.state.cvelist[i].length === 0) return '';
            return (
              <div className="card" id={lbl}>
                <div className="card-header" id={`heading${lbl}`}>
                  <h4 className="mb-0">
                    <button
                      className="btn btn-link"
                      type="button"
                      data-toggle="collapse"
                      data-target={`#collapse${lbl}`}
                      aria-controls={`collapse${lbl}`}
                    >
                      {label}
                    </button>
                  </h4>
                </div>

                <div id={`collapse${lbl}`} className="collapse" aria-labelledby={`#heading${lbl}`} data-parent="#accordionExample">
                  <div className="card-body">
                    <div className="table-responsive">
                      <table className="table table-striped">
                        <thead>
                          <tr>
                            <th>ID</th>
                            <th>Summary</th>
                            <th>Published</th>
                          </tr>
                        </thead>
                        <tbody>
                          {this.state.cvelist[i].map(cve => (
                            <tr id={cve}>
                              <td>
                                <Link to={`/cve/${cve.id}`}>{cve.id}</Link>
                              </td>
                              <td>{cve.summary}</td>
                              <td>{cve.published}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      );

    return (
      <>
        <div className="canvas-container">
          <Bar ref={this.props.forwardRef} data={this.state.chartData} options={this.options} type="bar" />
        </div>
        <Timescale
          mode={this.props.mode}
          show={this.props.show}
          expanded={this.props.expanded}
          changeData={this.changeData}
          url={this.props.url}
        />
        {ex}
      </>
    );
  }
}

TimeGraph.propTypes = {
  expanded: PropTypes.bool,
  xLabel: PropTypes.string,
  yLabel: PropTypes.string,
  url: PropTypes.string.isRequired,
  forwardRef: PropTypes.oneOfType([PropTypes.func, PropTypes.shape({ current: PropTypes.any })]),
  show: PropTypes.node,
  mode: PropTypes.string.isRequired,
};
TimeGraph.defaultProps = {
  expanded: false,
  xLabel: '',
  yLabel: '',
  forwardRef: null,
  show: timeShown.year,
};

export default TimeGraph;
