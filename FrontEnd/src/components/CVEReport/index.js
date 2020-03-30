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
import { BASE_URL } from '../../constants';
import CVSSCalculator from './CVSSCalculator';
import ScoreCircle from '../ScoreCircle';
import QuestionHelper from '../questionHelper';

/**
 * Report for a given CVE
 */
class CVEReport extends Component {
  constructor(props) {
    super(props);

    this.state = {
      cveData: {},
      cweData: {},
    };
  }

  componentDidMount() {
    fetch(`${BASE_URL}/api/v1/cves/info`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        cves: [this.props.CVEId],
      }),
    })
      .then(response => response.json())
      .then(data => {
        this.setState(prev => {
          return { ...prev, cveData: data.cves[this.props.CVEId], cweData: data.cwes[data.cves[this.props.CVEId].cwe] };
        });
      });
  }

  render() {
    return Object.keys(this.state.cveData).length !== 0 ? (
      <>
        <div className="card mb-5">
          <div className="card-header">
            <h5 className="m-0">Information</h5>
          </div>
          <div className="card-body">
            <h5>
              CVSS Score <ScoreCircle className="m-0 d-inline" number={this.state.cveData.cvss} />
            </h5>
            <h5>Description</h5>
            <p>{this.state.cveData.summary}</p>
            <h5>Published</h5>
            <p>{this.state.cveData.Published}</p>
            <h5>References</h5>
            <ul>
              <p>
                {this.state.cveData.references.map(ref => (
                  <li>
                    <a href={ref}>{ref}</a>
                  </li>
                ))}
              </p>
            </ul>
          </div>
        </div>
        <CVSSCalculator cvss={this.state.cveData.cvss} cvssVector={this.state.cveData['cvss-vector']} />
        {this.state.cweData !== undefined && Object.keys(this.state.cweData).length !== 0 ? (
          <div className="card mb-5">
            <div className="card-header">
              <h5 className="m-0">
                <QuestionHelper elaboration="shortcut_cwe">
                  <a href={`https://cwe.mitre.org/data/definitions/${this.state.cweData.id}.html`}> CWE</a>
                </QuestionHelper>{' '}
                {this.state.cweData.id}
              </h5>
            </div>
            <div className="card-body">
              <h5>{this.state.cweData.name}</h5>
              <p>{this.state.cweData.Description.slice(0, this.state.cweData.Description.length / 2)}</p>
            </div>
          </div>
        ) : (
          ''
        )}
      </>
    ) : (
      <div className="spinner-border" role="status">
        <span className="sr-only">Loading...</span>
      </div>
    );
  }
}

CVEReport.propTypes = {
  /** CVE id */
  CVEId: PropTypes.string.isRequired,
};

export default CVEReport;
