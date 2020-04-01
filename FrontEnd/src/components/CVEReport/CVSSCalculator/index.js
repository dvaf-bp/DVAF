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
/* eslint-disable no-restricted-syntax */
/* eslint-disable guard-for-in */

import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Spinner from 'react-bootstrap/Spinner';
import './style.scss';
import QuestionHelper from '../../questionHelper/index';

const BasicLayout = props => {
  return (
    <div className="card mb-5">
      <div className="card-header">
        <h5 className="m-0">
          <QuestionHelper elaboration="shortcut_cvss">CVSS</QuestionHelper> Vector
        </h5>
      </div>
      <div className="card-body">{props.children}</div>
    </div>
  );
};

BasicLayout.propTypes = {
  children: PropTypes.arrayOf(PropTypes.object),
};

BasicLayout.defaultProps = {
  children: [],
};

class CVSSCalculator extends Component {
  constructor(props) {
    super(props);
    // TODO: add unknown, unproven, none to scss
    this.severityEnum = {
      unknown: 'list-group-item-unknown',
      unproven: 'list-group-item-unproven',
      danger: 'list-group-item-danger',
      warning_plus: 'list-group-item-warning-plus',
      warning: 'list-group-item-warning',
      none: 'list-group-item-warning',
    };

    const CVSSLanguage = {
      v31: {
        regex: 'CVSS:3.1/AV:(.)/AC:(.)/PR:(.)/UI:(.)/S:(.)/C:(.)/I:(.)/A:(.)',
        metricLabels: ['S', 'AV', 'AC', 'PR', 'UI', 'C', 'I', 'A'],
        statesTree: [
          {
            name: 'Attack Vector',
            label: 'AV',
            possStates: [
              {
                name: 'Network',
                label: 'N',
                severity: this.severityEnum.danger,
              },
              {
                name: 'Adjacent',
                label: 'A',
                severity: this.severityEnum.warning_plus,
              },
              {
                name: 'Local',
                label: 'L',
                severity: this.severityEnum.warning,
              },
              {
                name: 'Physical',
                label: 'P',
                severity: this.severityEnum.warning,
              },
            ],
          },
          {
            name: 'Attack Complexity',
            possStates: [
              {
                name: 'High',
                label: 'H',
                severity: this.severityEnum.warning_plus,
              },
              {
                name: 'Low',
                label: 'L',
                severity: this.severityEnum.warning,
              },
            ],
          },
          {
            name: 'Privileges Required',
            possStates: [
              {
                name: 'None',
                label: 'N',
                severity: this.severityEnum.danger,
              },
              {
                name: 'Low',
                label: 'L',
                severity: this.severityEnum.warning_plus,
              },
              {
                name: 'High',
                label: 'H',
                severity: this.severityEnum.warning,
              },
            ],
          },
          {
            name: 'User Interaction',
            label: 'UI',
            possStates: [
              {
                name: 'None',
                label: 'N',
                severity: this.severityEnum.danger,
              },
              {
                name: 'Required',
                label: 'R',
                severity: this.severityEnum.warning,
              },
            ],
          },
          {
            name: 'Scope',
            label: 'S',
            possStates: [
              {
                name: 'Changed',
                label: 'C',
                severity: this.severityEnum.danger,
              },
              {
                name: 'Unchanged',
                label: 'C',
                severity: this.severityEnum.warning,
              },
            ],
          },
          {
            name: 'Confidentiality',
            label: 'C',
            possStates: [
              {
                name: 'High',
                label: 'H',
                severity: this.severityEnum.danger,
              },
              {
                name: 'Low',
                label: 'L',
                severity: this.severityEnum.warning_plus,
              },
              {
                name: 'None',
                label: 'N',
                severity: this.severityEnum.warning,
              },
            ],
          },
          {
            name: 'Integrity',
            label: 'I',
            possStates: [
              {
                name: 'High',
                label: 'H',
                severity: this.severityEnum.danger,
              },
              {
                name: 'Low',
                label: 'L',
                severity: this.severityEnum.warning_plus,
              },
              {
                name: 'None',
                label: 'N',
                severity: this.severityEnum.warning,
              },
            ],
          },
          {
            name: 'Availability',
            possStates: [
              {
                name: 'High',
                label: 'H',
                severity: this.severityEnum.warning_plus,
              },
              {
                name: 'Low',
                label: 'L',
                severity: this.severityEnum.warning,
              },
              {
                name: 'None',
                label: 'N',
                severity: this.severityEnum.none,
              },
            ],
          },
        ],
      },
      v3: {
        regex: 'CVSS:3.0/S:(.)/AV:(.)/AC:(.)/PR:(.)/UI:(.)/C:(.)/I:(.)/A:(.)/E:(.)/RL:(.)',
        metricLabels: ['S', 'AV', 'AC', 'PR', 'UI', 'C', 'I', 'A', 'E', 'RL'],
        statesTree: [
          {
            name: 'Attack Vector',
            label: 'AV',
            possStates: [
              {
                name: 'Network',
                label: 'N',
                severity: this.severityEnum.danger,
              },
              {
                name: 'Adjacent',
                label: 'A',
                severity: this.severityEnum.warning_plus,
              },
              {
                name: 'Local',
                label: 'L',
                severity: this.severityEnum.warning,
              },
              {
                name: 'Physical',
                label: 'P',
                severity: this.severityEnum.warning,
              },
            ],
          },
          {
            name: 'Attack Complexity',
            possStates: [
              {
                name: 'High',
                label: 'H',
                severity: this.severityEnum.warning_plus,
              },
              {
                name: 'Low',
                label: 'L',
                severity: this.severityEnum.warning,
              },
            ],
          },
          {
            name: 'Privileges Required',
            possStates: [
              {
                name: 'None',
                label: 'N',
                severity: this.severityEnum.danger,
              },
              {
                name: 'Low',
                label: 'L',
                severity: this.severityEnum.warning_plus,
              },
              {
                name: 'High',
                label: 'H',
                severity: this.severityEnum.warning,
              },
            ],
          },
          {
            name: 'User Interaction',
            label: 'UI',
            possStates: [
              {
                name: 'None',
                label: 'N',
                severity: this.severityEnum.danger,
              },
              {
                name: 'Required',
                label: 'R',
                severity: this.severityEnum.warning,
              },
            ],
          },
          {
            name: 'Scope',
            label: 'S',
            possStates: [
              {
                name: 'Changed',
                label: 'C',
                severity: this.severityEnum.danger,
              },
              {
                name: 'Unchanged',
                label: 'C',
                severity: this.severityEnum.warning,
              },
            ],
          },
          {
            name: 'Confidentiality',
            label: 'C',
            possStates: [
              {
                name: 'High',
                label: 'H',
                severity: this.severityEnum.danger,
              },
              {
                name: 'Low',
                label: 'L',
                severity: this.severityEnum.warning_plus,
              },
              {
                name: 'None',
                label: 'N',
                severity: this.severityEnum.warning,
              },
            ],
          },
          {
            name: 'Integrity',
            label: 'I',
            possStates: [
              {
                name: 'High',
                label: 'H',
                severity: this.severityEnum.danger,
              },
              {
                name: 'Low',
                label: 'L',
                severity: this.severityEnum.warning_plus,
              },
              {
                name: 'None',
                label: 'N',
                severity: this.severityEnum.warning,
              },
            ],
          },
          {
            name: 'Availability',
            possStates: [
              {
                name: 'High',
                label: 'H',
                severity: this.severityEnum.warning_plus,
              },
              {
                name: 'Low',
                label: 'L',
                severity: this.severityEnum.warning,
              },
              {
                name: 'None',
                label: 'N',
                severity: this.severityEnum.none,
              },
            ],
          },
          {
            name: 'Exploit Code Maturity',
            possStates: [
              {
                name: 'Not Defined',
                label: 'X',
                severity: this.severityEnum.warning_plus,
              },
              {
                name: 'Unproven',
                label: 'U',
                severity: this.severityEnum.warning,
              },
              {
                name: 'Proof-of-Concept',
                label: 'P',
                severity: this.severityEnum.none,
              },
              {
                name: 'Functional',
                label: 'F',
                severity: this.severityEnum.none,
              },
              {
                name: 'High',
                label: 'H',
                severity: this.severityEnum.none,
              },
            ],
          },
          {
            name: 'Remediation Level',
            possStates: [
              {
                name: 'Not Defined',
                label: 'X',
                severity: this.severityEnum.warning_plus,
              },
              {
                name: 'Official Fix',
                label: 'O',
                severity: this.severityEnum.warning,
              },
              {
                name: 'Temporary Fix',
                label: 'T',
                severity: this.severityEnum.none,
              },
              {
                name: 'Workaround',
                label: 'W',
                severity: this.severityEnum.none,
              },
              {
                name: 'Unavailable',
                label: 'U',
                severity: this.severityEnum.none,
              },
            ],
          },
          {
            name: 'Report Confidence',
            possStates: [
              {
                name: 'Not Defined',
                label: 'X',
                severity: this.severityEnum.unknown,
              },
              {
                name: 'Unkown',
                label: 'U',
                severity: this.severityEnum.unknown,
              },
              {
                name: 'Reasonable',
                label: 'R',
                severity: this.severityEnum.warning_plus,
              },
              {
                name: 'Confirmed',
                label: 'C',
                severity: this.severityEnum.danger,
              },
            ],
          },
        ],
      },
      v2: {
        regex: 'AV:(.)/AC:(.)/Au:(.)/C:(.)/I:(.)/A:(.)',
        metricLabels: ['AV', 'AC', 'Au', 'C', 'I', 'A'],
        statesTree: [
          {
            name: 'Attack Vector',
            label: 'AV',
            possStates: [
              {
                name: 'Network',
                label: 'N',
                severity: this.severityEnum.danger,
              },
              {
                name: 'Adjacent',
                label: 'A',
                severity: this.severityEnum.warning_plus,
              },
              {
                name: 'Local',
                label: 'L',
                severity: this.severityEnum.warning,
              },
              {
                name: 'Physical',
                label: 'P',
                severity: this.severityEnum.warning,
              },
            ],
          },
          {
            name: 'Attack Complexity',
            label: 'AC',
            possStates: [
              {
                name: 'High',
                label: 'H',
                severity: this.severityEnum.warning,
              },
              {
                name: 'Medium',
                label: 'M',
                severity: this.severityEnum.warning_plus,
              },
              {
                name: 'Low',
                label: 'L',
                severity: this.severityEnum.danger,
              },
            ],
          },
          {
            name: 'Authentication',
            label: 'Au',
            possStates: [
              {
                name: 'Multiple',
                label: 'M',
                severity: this.severityEnum.warning,
              },
              {
                name: 'Single',
                label: 'S',
                severity: this.severityEnum.warning_plus,
              },
              {
                name: 'None',
                label: 'N',
                severity: this.severityEnum.danger,
              },
            ],
          },
          {
            name: 'Confidentiality Impact',
            label: 'C',
            possStates: [
              {
                name: 'Complete',
                label: 'C',
                severity: this.severityEnum.danger,
              },
              {
                name: 'Partial',
                label: 'P',
                severity: this.severityEnum.warning_plus,
              },
              {
                name: 'None',
                label: 'N',
                severity: this.severityEnum.warning,
              },
            ],
          },
          {
            name: 'Integrity Impact',
            label: 'I',
            possStates: [
              {
                name: 'Complete',
                label: 'C',
                severity: this.severityEnum.danger,
              },
              {
                name: 'Partial',
                label: 'P',
                severity: this.severityEnum.warning_plus,
              },
              {
                name: 'None',
                label: 'N',
                severity: this.severityEnum.warning,
              },
            ],
          },
          {
            name: 'Availability Impact',
            label: 'A',
            possStates: [
              {
                name: 'Complete',
                label: 'C',
                severity: this.severityEnum.danger,
              },
              {
                name: 'Partial',
                label: 'P',
                severity: this.severityEnum.warning_plus,
              },
              {
                name: 'None',
                label: 'N',
                severity: this.severityEnum.warning,
              },
            ],
          },
        ],
      },
    };

    let vectorVersion;
    let match;

    for (const version in CVSSLanguage) {
      const versionInfos = CVSSLanguage[version];

      const re = new RegExp(versionInfos.regex);
      match = re.exec(this.props.cvssVector);

      if (re.test(this.props.cvssVector)) {
        vectorVersion = version;
        break;
      }
    }

    if (vectorVersion === undefined) {
      console.error(`CVSS-Vector-Version isn't defined: ${this.props.cvssVector}`);
      this.state = {
        language: undefined,
        versionOfVector: undefined,
        stateOfCVSS: undefined,
      };
      return;
    }

    this.state = {
      language: CVSSLanguage,
      versionOfVector: vectorVersion,
      stateOfCVSS: match.slice(1).map((metricValue, metricLabelIndex) => {
        return [CVSSLanguage[vectorVersion].metricLabels[metricLabelIndex], metricValue];
      }),
    };
  }

  isOn(currStateLabel, currMetricLabel) {
    return (
      this.state.stateOfCVSS.filter(
        ([actualStateLabelWalter, actualStateMetricLabelWalker]) =>
          currStateLabel === actualStateLabelWalter && currMetricLabel === actualStateMetricLabelWalker,
      ).length > 0
    );
  }

  render() {
    // In the Database, there is no CVSS-Vector provided by the parent;
    // This means probbably, that the CVE has not yet a CVE-Vector attributed by NVD.
    // THE Authorities need some time to attribute CVE-Vectors to CVEs
    if (this.props.cvssVector === '') {
      return (
        <BasicLayout>
          <p>There is no information about this CVE available yet. </p>
        </BasicLayout>
      );
    }
    // if the state isn't undefined and but the length of stateOfCVSS is 0, then the data is still loading/ calculating
    if (this.state !== undefined && this.state.stateOfCVSS.length === 0) {
      return (
        <BasicLayout>
          <Spinner />
        </BasicLayout>
      );
    }

    return (
      <BasicLayout>
        <div className="d-flex flex-wrap justify-content-around">
          {this.state.language[this.state.versionOfVector].statesTree.map(currState => (
            <div className="card border-light" style={{ maxWidth: '15rem' }}>
              <div className="card-header">{currState.name}</div>
              <div className="card-body">
                <ul className="list-group">
                  {currState.possStates.map(({ name: currMetricName, label: currMetricLabel, severity: currMetricSeverity }) => (
                    <li
                      className={`list-group-item ${currMetricSeverity} ${this.isOn(currState.label, currMetricLabel) ? '' : 'disabled'}`}
                    >
                      <i className={`icon-${currState.label}${currMetricName}`} />
                      {currMetricName}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </BasicLayout>
    );
  }
}

CVSSCalculator.propTypes = {
  cvssVector: PropTypes.string,
};

CVSSCalculator.defaultProps = {
  cvssVector: '',
};

export default CVSSCalculator;
