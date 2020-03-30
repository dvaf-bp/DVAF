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
import Spinner from 'react-bootstrap/Spinner';
import './style.scss';

class CVSSCalculator extends Component {
  constructor(props) {
    super(props);

    this.cvss = {
      'Attack Vector': [
        ['Network', 2],
        ['Adjacent', 1],
        ['Local', 0],
        ['Physical', 0],
      ],
      'Attack Complexity': [
        ['Low', 2],
        ['Medium', 1],
        ['High', 0],
      ],
      'Privileges Required': [
        ['None', 2],
        ['Low', 1],
        ['High', 0],
      ],
      'User Interaction': [
        ['None', 2],
        ['Required', 0],
      ],
      Scope: [
        ['Changed', 2],
        ['Unchanged', 0],
      ],
      Confidentiality: [
        ['High', 2],
        ['Low', 1],
        ['None', 0],
      ],
      Integrity: [
        ['High', 2],
        ['Low', 1],
        ['None', 0],
      ],
      Availability: [
        ['High', 2],
        ['Low', 1],
        ['None', 0],
      ],
    };

    this.severityEnum = {
      2: 'list-group-item-danger',
      1: 'list-group-item-warning-plus',
      0: 'list-group-item-warning',
    };
  }

  fieldIsSet(code, v) {
    let retval = false;
    this.props.cvssVector.split('/').forEach(e => {
      if (e.startsWith(`${code}:`)) {
        v.forEach(val => {
          if (e.endsWith(val[0].charAt(0))) retval = true;
        });
      }
    });

    return retval;
  }

  render() {
    return this.props.cvssVector !== '' ? (
      <div className="card mb-5">
        <div className="card-header">
          <h5 className="m-0">CVSS Score</h5>
        </div>
        <div className="card-body">
          <div className="d-flex flex-wrap justify-content-around">
            {Object.entries(this.cvss).map(([k, v]) => {
              const code = k
                .split(' ')
                .map(s => s.charAt(0))
                .join('');

              if (!this.fieldIsSet(code, v)) return '';

              return (
                <div className="card border-light m-1" style={{ maxWidth: '15rem' }}>
                  <div className="card-header">{k}</div>
                  <div className="card-body">
                    <ul className="list-group">
                      {v.map(([str, severity]) => {
                        const isOn = this.props.cvssVector.includes(`${code}:${str.charAt(0)}`);
                        return (
                          <li className={`list-group-item ${this.severityEnum[severity]} ${isOn ? '' : 'disabled'}`}>
                            <i className={`icon-${code}${str}`} />
                            {str}
                          </li>
                        );
                      })}
                    </ul>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    ) : (
      <Spinner />
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
