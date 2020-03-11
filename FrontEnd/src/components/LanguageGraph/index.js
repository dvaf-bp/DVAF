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
import { Pie } from 'react-chartjs-2';
import 'chartjs-plugin-colorschemes';
import GraphSwitch from '../GraphSwitch';

class LanguageGraph extends Component {
  constructor(props) {
    super(props);

    this.state = {
      smallData: {
        labels: [],
        datasets: [
          {
            data: [0],
          },
        ],
      },
      expandedData: {
        labels: [],
        datasets: [
          {
            data: [0],
          },
        ],
      },
      sloc: [],
      expanded: this.props.expanded,
    };
    this.initialState = { ...this.state };

    this.options = {
      responsive: true,
      maintainAspectRatio: false,
      legend: {
        display: true,
      },
      plugins: {
        colorschemes: {
          scheme: 'office.Parallax6',
        },
      },
    };

    uniqueId.enableUniqueIds(this);
  }

  componentDidMount() {
    const smallLabels = [];
    const smallSlocs = [];
    let total = 0;

    Object.values(this.props.slocs).forEach(val => {
      const name = val[0];
      const sloc = val[1];

      total += sloc;

      if (smallLabels.length < 4) {
        smallLabels.push(name);
        smallSlocs.push(sloc);
      } else if (smallLabels.length === 4) {
        smallLabels.push('Other');
        smallSlocs.push(sloc);
      } else smallSlocs[4] += sloc;
    });

    Object.values(this.props.slocs).forEach(e => {
      const res = `${((e[1] / total) * 100).toFixed(2)}%`;
      if (res === '0.00%') e.push('<0.01%');
      else e.push(res);
    });

    this.setState(prev => {
      const newState = { ...prev };
      newState.smallData.labels = smallLabels;
      newState.smallData.datasets[0].data = smallSlocs;
      newState.expandedData.labels = this.props.slocs.map(e => e[0]);
      newState.expandedData.datasets[0].data = this.props.slocs.map(e => e[1]);
      return newState;
    });
  }

  componentDidUpdate(prevProps) {
    if (prevProps === this.props) return;

    this.reset();
  }

  reset() {
    this.setState(this.initialState, this.componentDidMount);
  }

  render() {
    return (
      <>
        {this.props.expandable ? <GraphSwitch defaultChecked={this.state.expanded} onChange={e => this.setState({ expanded: e })} /> : ''}

        {this.state.expanded ? (
          <table className="table table-striped mt-4">
            <thead>
              <tr>
                <th>Language</th>
                <th>LOC</th>
                <th>Percentage</th>
              </tr>
            </thead>
            <tbody>
              {this.props.slocs.map(sloc => (
                <tr key={sloc[0]}>
                  <td>{sloc[0]}</td>
                  <td>{sloc[1]}</td>
                  <td>{sloc[2]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="canvas-container">
            <Pie ref={this.props.forwardRef} data={this.state.smallData} options={this.options} />
          </div>
        )}
      </>
    );
  }
}

LanguageGraph.propTypes = {
  expanded: PropTypes.bool,
  slocs: PropTypes.node.isRequired,
  forwardRef: PropTypes.oneOfType([PropTypes.func, PropTypes.shape({ current: PropTypes.any })]),
  expandable: PropTypes.bool,
};
LanguageGraph.defaultProps = {
  expanded: false,
  forwardRef: null,
  expandable: true,
};

export default LanguageGraph;
