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
import Listing from '../../components/Listing';
import BoxTitle from '../../components/Box/BoxTitle';
import './package.scss';
import TimeGraph from '../../components/TimeGraph';
import LanguageGraph from '../../components/LanguageGraph';
import { BASE_URL } from '../../constants';
import { timeShown } from '../../components/TimeGraph/timescale';

class Package extends Component {
  constructor(props) {
    super(props);

    this.state = {
      versions: [],
      dependencies: [],
      similarPackages: [],
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
        const { description } = pkg;

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
          newState.description = description;
          return newState;
        });
      })
      .catch(e => console.error(e));

    fetch(`${BASE_URL}/api/v1/packages/match/${this.props.match.params.name}`)
      .then(response => response.json())
      .then(apiSimPkg => {
        this.setState(prev => {
          const newState = { ...prev };
          newState.similarPackages = apiSimPkg.map(pkg => pkg.name);
          return newState;
        });
      })
      // eslint-disable-next-line no-console
      .catch(e => console.log(e));
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
        <PageTitle backLink={this.props.location.query ? `/search?query=${this.props.location.query}` : '/search'}>
          {this.props.match.params.name}
        </PageTitle>
        <i> {this.state.description} </i>
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
          <GraphContainer title="Languages">
            <LanguageGraph slocs={this.state.slocs} />
          </GraphContainer>
          <Box>
            <BoxTitle>Dependencies</BoxTitle>
            <Listing emptyMessage="This package has no build dependencies." list={this.state.dependencies} />
          </Box>
          {this.state.similarPackages.length > 1 ? (
            <Box>
              <BoxTitle>Similar Packages</BoxTitle>
              <Listing emptyMessage="No similar packages in Database." list={this.state.similarPackages} />
            </Box>
          ) : (
            <> </>
          )}
        </section>
        <GraphContainer title="Vulnerabilities versus Time">
          <TimeGraph
            mode="package"
            show={timeShown.month}
            chartUrl={`/api/v1/packages/cves/count/${this.props.match.params.name}`}
            tableUrl={`/api/v1/packages/cves/${this.props.match.params.name}`}
          />
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
  location: PropTypes.shape({
    query: PropTypes.string.isRequired,
  }).isRequired,
};

export default Package;
