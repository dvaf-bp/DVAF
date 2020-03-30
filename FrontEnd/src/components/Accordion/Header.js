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

/**
 * Accordion Header
 */
const Header = props => {
  return (
    <div className="card-header" id={`heading${props.for}`}>
      <h2 className="mb-0">
        <button
          className="btn btn-link"
          type="button"
          data-toggle="collapse"
          data-target={`#collapse${props.for}`}
          aria-controls={`collapse${props.for}`}
          disabled={props.disabled}
        >
          {props.children}
        </button>
      </h2>
    </div>
  );
};

Header.propTypes = {
  /** If true, the header is disabled and therefore not clickable */
  disabled: PropTypes.bool,
  /** Entry Id: connects Head to Content */
  for: PropTypes.string.isRequired,
  /** Header Content, e.g. Text */
  children: PropTypes.node.isRequired,
};

Header.defaultProps = {
  disabled: false,
};

export default Header;
