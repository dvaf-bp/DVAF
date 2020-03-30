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
import React from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import TimeGraph from '../../../components/TimeGraph';
import PageTitle from '../../../components/pagetitle';
import GraphContainer from '../../../components/GraphContainer';
import { timeShown } from '../../../components/timescale';

const VulnView = props => {
  return (
    <>
      <PageTitle>
        <Link to={`../${props.match.params.name}`}>{props.match.params.name}</Link> / Vulnerabilities
      </PageTitle>
      <GraphContainer title="">
        <TimeGraph mode="package" show={timeShown.month} expanded url={`/api/v1/packages/cves/${props.match.params.name}`} />
      </GraphContainer>
    </>
  );
};

VulnView.propTypes = {
  match: PropTypes.shape({
    params: PropTypes.shape({
      name: PropTypes.string,
    }).isRequired,
  }).isRequired,
};

export default VulnView;
