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
import { Link } from 'react-router-dom';
import PageTitle from '../../../components/pagetitle';
import LanguageGraph from '../../../components/LanguageGraph';
import GraphContainer from '../../../components/GraphContainer';
import 'chartjs-plugin-colorschemes';
import { BASE_URL } from '../../../constants';

class LanguageView extends Component {
  constructor(props) {
    super(props);

    this.state = {
      slocs: [],
    };
  }

  componentDidMount() {
    fetch(`${BASE_URL}/api/v1/packages/${this.props.match.params.name}`)
      .then(response => response.json())
      .then(pkg => {
        this.setState(prev => {
          const newState = { ...prev };
          newState.slocs = Object.entries(pkg.versions[0].sloc).sort((a, b) => {
            return b[1] - a[1];
          });
          return newState;
        });
      })
      .catch(e => console.error(e));
  }

  render() {
    return (
      <>
        <PageTitle>
          <Link to={`../${this.props.match.params.name}`}>{this.props.match.params.name}</Link> / Languages
        </PageTitle>
        <GraphContainer title="">
          <LanguageGraph expanded slocs={this.state.slocs} />
        </GraphContainer>
      </>
    );
  }
}

LanguageView.propTypes = {
  match: PropTypes.shape({
    params: PropTypes.shape({
      name: PropTypes.string,
    }).isRequired,
  }).isRequired,
};

export default LanguageView;
