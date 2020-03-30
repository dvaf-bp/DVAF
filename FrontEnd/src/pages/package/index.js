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
import PageTitle from '../../components/pagetitle';
import Box from '../../components/Box';
import GraphContainer from '../../components/GraphContainer';
import 'chartjs-plugin-colorschemes';
import Dependencies from '../../components/Dependencies';
import BoxTitle from '../../components/Box/BoxTitle';
import './package.scss';
import TimeGraph from '../../components/TimeGraph';
import LanguageGraph from '../../components/LanguageGraph';
import { BASE_URL } from '../../constants';
import { timeShown } from '../../components/timescale';

class Package extends Component {
  constructor(props) {
    super(props);

    this.state = {
      versions: [],
      dependencies: [],
      lang_data: {
        labels: [],
        datasets: [
          {
            data: [0],
          },
        ],
      },
      slocs: [],
    };
    this.initialState = { ...this.state };
  }

  componentDidMount() {
    fetch(`${BASE_URL}/api/v1/packages/${this.props.match.params.name}`)
      .then(response => response.json())
      .then(pkg => {
        const { versions } = pkg;
        const versionResults = [];
        const dependencies = pkg.versions[0].build_depends;

        versions.forEach(version => {
          versionResults.push([version.suites.join(', '), version.version]);
        });

        this.setState(prev => {
          const newState = { ...prev };
          newState.versions = versionResults;
          newState.slocs = Object.entries(pkg.versions[0].sloc).sort((a, b) => {
            return b[1] - a[1];
          });
          newState.dependencies = dependencies;
          return newState;
        });
      })
      .catch(e => console.error(e));
  }

  componentDidUpdate(prevProps) {
    if (this.props.match.params.name === prevProps.match.params.name) return;
    this.reset();
  }

  reset() {
    this.setState(this.initialState, this.componentDidMount());
  }

  render() {
    return (
      <>
        <PageTitle>{this.props.match.params.name}</PageTitle>
        <section className="package-page">
          <Box>
            <BoxTitle>Versions</BoxTitle>

            <table className="table table-striped">
              <tbody>
                {this.state.versions.map(version => (
                  <tr key={version[0]}>
                    <td>
                      <strong>{version[0]}</strong>
                    </td>
                    <td>
                      <span>{version[1]}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Box>
          <GraphContainer title="Languages" to={`${this.props.match.params.name}/languages`}>
            <LanguageGraph slocs={this.state.slocs} />
          </GraphContainer>
          <Box>
            <BoxTitle>Dependencies</BoxTitle>
            <Dependencies dependencies={this.state.dependencies} />
          </Box>
        </section>
        <GraphContainer title="Vulnerabilities versus Time" to={`${this.props.match.params.name}/vuln`}>
          <TimeGraph mode="package" show={timeShown.month} url={`/api/v1/packages/cves/count/${this.props.match.params.name}`} />
        </GraphContainer>
      </>
    );
  }
}

Package.propTypes = {
  match: PropTypes.shape({
    params: PropTypes.shape({
      name: PropTypes.string,
    }).isRequired,
  }).isRequired,
};

export default Package;
