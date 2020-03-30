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
import Spinner from 'react-bootstrap/Spinner';
import PageTitle from '../../components/pagetitle';
import SpaceAround from '../../components/SpaceAround';
import Box from '../../components/Box';
import GraphContainer from '../../components/GraphContainer';
import TimeGraph from '../../components/TimeGraph';
import { BASE_URL } from '../../constants';
import InformationHelper from '../../components/InformationHelper';
import NormalMode from '../../components/TimeGraph/modes/Normal';

class Dashboard extends Component {
  constructor(props) {
    super(props);

    this.state = {
      DashboardData: null,
    };
  }

  componentDidMount() {
    const today = new Date();
    const dd = String(today.getDate()).padStart(2, '0');
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const yyyy = today.getFullYear();
    const weekBefore = new Date(today);
    weekBefore.setDate(today.getDate() - 14);
    const ddBefore = String(weekBefore.getDate()).padStart(2, '0');
    const mmBefore = String(weekBefore.getMonth() + 1).padStart(2, '0');
    const yyyyBefore = weekBefore.getFullYear();

    fetch(`${BASE_URL}/api/v1/dashboard/cves/${ddBefore}-${mmBefore}-${yyyyBefore}/${dd}-${mm}-${yyyy}/day`)
      .then(response => response.json())
      .then(data => {
        const cveData = data.cves.slice(7).flat();
        const lastSevenDays = cveData.length;
        const flatten = data.cves.flat();
        const newestCVE = flatten.length === 0 ? { id: '' } : flatten[flatten.length - 1];
        const compareWeeks = lastSevenDays - data.cves.slice(0, 6).flat().length;

        this.setState({
          DashboardData: {
            newestCVE,
            lastSevenDays,
            compareWeeks,
          },
        });
      });
  }

  render() {
    const dashData = this.state.DashboardData;
    const spinner = <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />;
    const newestCVE = !dashData ? spinner : <Link to={`/cve/${dashData.newestCVE.id}`}>{dashData.newestCVE.id}</Link>;
    const lastSevenDays = !dashData ? spinner : dashData.lastSevenDays;
    const compareWeeks = !dashData ? spinner : dashData.compareWeeks;

    return (
      <>
        <PageTitle>General</PageTitle>
        <SpaceAround>
          <Box>
            <span className="bignum">{newestCVE}</span>
            <span className="subtitle">
              <b>most recent CVE</b> <br />
              published
            </span>
          </Box>
          <Box>
            <span className="bignum">{lastSevenDays}</span>
            <span className="subtitle">
              <b>published CVEs</b> <br />
              in the last 7 days
            </span>
          </Box>
          <Box>
            <span className="bignum">{compareWeeks}</span>
            <span className="subtitle">
              <b>vulnerabilities found</b>
              <br />
              in comparison to the week before
            </span>
          </Box>
        </SpaceAround>
        <GraphContainer title="Vulnerabilities versus Time">
          <TimeGraph expandable={false} mode={NormalMode} chartUrl="/api/v1/dashboard/cves/count" />
          <InformationHelper template="nvd" />
        </GraphContainer>
      </>
    );
  }
}

export default Dashboard;
