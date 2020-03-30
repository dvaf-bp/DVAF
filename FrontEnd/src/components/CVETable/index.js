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
import { Link } from 'react-router-dom';

/**
 * Converts a list of CVEs to a table
 */
const CVETable = props => {
  return (
    <div className="table-responsive">
      <table className="table table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Summary</th>
            <th>Published</th>
          </tr>
        </thead>
        <tbody>
          {(props.cves || []).map((cve, i) => (
            <tr key={String(i) + cve.id}>
              <td>
                <Link to={`/cve/${cve.id}`}>{cve.id}</Link>
              </td>
              <td>{cve.summary}</td>
              <td>{cve.published}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

CVETable.propTypes = {
  /** CVEs response from API */
  cves: PropTypes.objectOf(
    PropTypes.shape({
      id: PropTypes.string,
      summary: PropTypes.string,
      published: PropTypes.string,
    }),
  ).isRequired,
};

export default CVETable;
