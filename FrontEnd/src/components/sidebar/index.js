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
import './index.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import Entry from './entry';

const Sidebar = props => {
  return (
    <aside className={`sidebar ${!props.open && 'sidebar-hide'}`}>
      <header>
        <button type="button" className="btn" onClick={props.click}>
          <FontAwesomeIcon icon={['fas', 'times']} />
        </button>
        <Link to="/">
          <img src="/DVAF_Logo.png" alt="DVAF-Logo" style={{ width: '100%', height: '100%' }} />
        </Link>
      </header>
      <ul className="nav flex-column">
        <Entry exact to="/" icon="home">
          General
        </Entry>
        <Entry to="/search" icon="search">
          Search
        </Entry>
        <Entry to="/scan" icon="upload">
          Scan Packages
        </Entry>
        <Entry to="/info" icon="book">
          Information
        </Entry>
        <Entry to="/export" icon="file-export">
          Export Data
        </Entry>
      </ul>
    </aside>
  );
};

Sidebar.propTypes = {
  click: PropTypes.func.isRequired,
  open: PropTypes.bool.isRequired,
};

export default Sidebar;
