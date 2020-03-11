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
import { NavLink } from 'react-router-dom';
import ScoreCircle from '../ScoreCircle';

const CVEEntry = props => {
  return (
    <div key={props.name} className="card mb-2">
      <div className="card-body d-flex align-items-center justify-content-between">
        <NavLink to={{ pathname: `/cve/${props.name}`, query: props.query }}>
          <h4 className="card-title">{props.name}</h4>
          <p className="card-text text-secondary">{props.desc}</p>
        </NavLink>
        <div className="text-center">
          CVSS Score:
          <ScoreCircle number={props.cvss} />
        </div>
      </div>
    </div>
  );
};

CVEEntry.propTypes = {
  name: PropTypes.string.isRequired,
  query: PropTypes.string.isRequired,
  desc: PropTypes.string.isRequired,
  cvss: PropTypes.number.isRequired,
};

export default CVEEntry;
