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
import PropTypes from 'prop-types';
import PageTitle from '../../components/pagetitle';
import CVETable from '../../components/CVETable';
import Accordion from '../../components/Accordion';
import AccordionHeader from '../../components/Accordion/Header';
import AccordionContent from '../../components/Accordion/Content';
import AccordionContainer from '../../components/Accordion/Container';
import PolarExtra from '../../components/PolarExtra';

const Results = props => {
  if (!props.location.cves)
    return (
      <>
        <PageTitle>Results</PageTitle>
        <div className="alert alert-success" role="alert">
          No open vulnerabilities found.
        </div>
      </>
    );

  const usableEntries = Object.entries(props.location.polar_chart).filter(
    e => e[0] !== 'rest' && e[0] !== 'total_cve_count' && Math.min(...Object.values(e[1])) !== 0,
  );
  const filterPolar = filter => usableEntries.filter(e => e[0] !== 'rest' && e[0] !== 'total_cve_count').map(e => e[1][filter]);

  return (
    <>
      <PageTitle>Results</PageTitle>
      <div className="mb-4">
        <PolarExtra
          data={{
            labels: usableEntries.map(e => e[0]),
            datasets: [
              {
                width: filterPolar('max_severity'),
                length: filterPolar('cve_count'),
                color: filterPolar('avg_severity'),
              },
            ],
          }}
          options={{
            text: '',
            colorBase: 10,
            widthBase: 10,
            alwaysShowLabel: true,
            lengthLabel: 'total CVE count',
            widthLabel: 'highest severity',
            colorLabel: 'average severity',
            opacity: 0.5,
          }}
        />
      </div>
      <Accordion id="cve_results">
        {Object.entries(props.location.cves)
          .sort((a, b) => b[1].open_cve_count - a[1].open_cve_count)
          .map(([pkg, cves]) => {
            const len = cves.open_cve_count;
            return (
              <AccordionContainer key={pkg}>
                <AccordionHeader disabled={len === 0} for={pkg}>
                  {pkg}
                  <span className={`ml-2 badge badge-${len === 0 ? 'success' : 'danger'}`}>
                    {len} open vulnerabilit{len !== 1 ? 'ies' : 'y'}
                  </span>
                </AccordionHeader>
                {len === 0 ? (
                  ''
                ) : (
                  <AccordionContent for={pkg} parent="cve_results">
                    <CVETable cves={cves.open_cves} />
                  </AccordionContent>
                )}
              </AccordionContainer>
            );
          })}
      </Accordion>
    </>
  );
};

Results.propTypes = {
  location: PropTypes.shape({
    pathname: PropTypes.string,
    cves: PropTypes.objectOf(PropTypes.arrayOf(PropTypes.string)),
    polar_chart: PropTypes.objectOf(
      PropTypes.objectOf(PropTypes.shape({ avg_severity: PropTypes.number, cve_count: PropTypes.number, max_severity: PropTypes.number })),
    ),
  }),
};

Results.defaultProps = {
  location: {
    pathname: '/results',
    cves: undefined,
  },
};

export default Results;
