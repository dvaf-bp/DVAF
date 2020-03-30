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
 * Accordion
 */
const Accordion = props => {
  return (
    <div className={`accordion ${props.className}`} id={props.id} style={props.style}>
      {props.children}
    </div>
  );
};

Accordion.propTypes = {
  /** Contains (multiple) AccordionContainer */
  children: PropTypes.node.isRequired,
  /** ID to identify this accordion */
  id: PropTypes.string.isRequired,
  /** Forward classes to accordion div */
  className: PropTypes.string,
  // this is the default type for style
  /** Forward style to accordion div */
  // eslint-disable-next-line
  style: PropTypes.object,
};
Accordion.defaultProps = {
  className: '',
  style: null,
};

export default Accordion;
