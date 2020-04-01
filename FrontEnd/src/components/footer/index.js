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

/**
 * Footer of the website
 */
class Footer extends Component {
  constructor(props) {
    super(props);

    this.state = {
      response: null,
    };
  }

  componentDidMount() {
    fetch(`${BASE_URL}/api/v1/meta/last_updated`)
      .then(response => response.json())
      .then(data => {
        this.setState({ response: data });
      })
      .catch(e => console.error(e));
  }

  render() {
    return (
      <footer className={this.props.className}>
        <hr />
        <div className="row align-items-center">
          <div className="col-sm">
            © 2020 Copyright: DVAF
            <img
              className="ml-1"
              src="https://travis-ci.com/mowirth/dvaf-frontend.svg?token=3pYLhWgBdLmhyWCVPfCP&branch=dev"
              alt="build status"
            />
          </div>
          {this.state.response && (
            <div className="col-sm text-center">
              {Object.prototype.hasOwnProperty.call(this.state.response, 'cvedb') && (
                <small className="text-muted">Last CVE update: {this.state.response.cvedb.cves.last_updated}</small>
              )}
              <br />
              {Object.prototype.hasOwnProperty.call(this.state.response, 'debian') && (
                <small className="text-muted">Last package update: {this.state.response.debian.last_updated}</small>
              )}
            </div>
          )}
          <div className="col-sm">
            <div className="float-right">
              <a href="./dsgvo">DSGVO</a> | <a href="./imprint">Imprint</a> | <a href="https://github.com/dvaf-bp/dvaf">Source Code</a>
              <a href="https://tu-darmstadt.de">
                <img src="/tud_logo.gif" className="ml-2" alt="TU Darmstadt Logo" style={{ height: '50px' }} />
              </a>
            </div>
          </div>
        </div>
      </footer>
    );
  }
}

Footer.propTypes = {
  /** Passes className to footer tag */
  className: PropTypes.string,
};
Footer.defaultProps = {
  className: 'pt-3 ',
};

export default Footer;
