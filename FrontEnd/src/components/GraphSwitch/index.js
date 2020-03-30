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
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import './GraphSwitch.scss';

/**
 * Switch to change between the graph view and the table view
 */
class GraphSwitch extends Component {
  constructor(props) {
    super(props);

    this.state = {
      expanded: this.props.defaultChecked,
    };
  }

  render() {
    return (
      <div className="btn-group btn-group-sm graphSwitch" role="group">
        <button
          type="button"
          onClick={() => {
            this.setState({ expanded: false });
            this.props.onChange(false);
          }}
          className={!this.state.expanded ? 'btn btn-secondary' : 'btn btn-outline-secondary'}
          title="Switch to graph view"
        >
          <FontAwesomeIcon icon={('fas', 'chart-bar')} />
        </button>
        <button
          type="button"
          onClick={() => {
            this.setState({ expanded: true });
            this.props.onChange(true);
          }}
          className={this.state.expanded ? 'btn btn-secondary' : 'btn btn-outline-secondary'}
          title="Switch to table view"
        >
          <FontAwesomeIcon icon={('fas', 'table')} />
        </button>
      </div>
    );
  }
}

GraphSwitch.propTypes = {
  /** If true, table is shown by default */
  defaultChecked: PropTypes.bool.isRequired,
  /** Function with a boolean parameter, which is called on change  */
  onChange: PropTypes.func.isRequired,
};

export default GraphSwitch;
