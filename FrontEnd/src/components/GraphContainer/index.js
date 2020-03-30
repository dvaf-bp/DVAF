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
import { saveAs } from 'file-saver';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import './graphcontainer.scss';
import PropTypes from 'prop-types';
import ReactResizeDetector from 'react-resize-detector';

/**
 * Container for graphs. Provides the box around, resize and download button.
 */
class GraphContainer extends Component {
  constructor(props) {
    super(props);

    this.canvas = null;
    this.height = null;

    this.chartRef = React.createRef();
    this.thisRef = React.createRef();

    this.download = this.download.bind(this);
    this.triggerResize = this.triggerResize.bind(this);

    this.state = {
      minHeight: 0,
    };
  }

  componentDidMount() {
    this.setState({ minHeight: this.thisRef.current.offsetHeight });
  }

  /**
   * Called on resize. Calls resize on chartjs graph.
   */
  triggerResize() {
    if (this.chartRef.current == null) return;

    this.chartRef.current.chartInstance.resize();
  }

  /**
   * Converts to the desired format and triggers the download dialog
   * @param {*} event click event
   */
  download(event) {
    if (this.chartRef.current == null) return;

    const image = this.chartRef.current.chartInstance.canvas.toDataURL(`image/${event.target.innerText}`);
    saveAs(image, this.props.title.split(' ').join('_'));
  }

  render() {
    const Heading = () => {
      if (this.props.to !== undefined)
        return (
          <Link to={this.props.to}>
            <h5>{this.props.title}</h5>
          </Link>
        );
      return <h5>{this.props.title}</h5>;
    };

    let clazz = 'graph';
    const childs = React.Children.map(this.props.children, child => {
      if (Object.prototype.hasOwnProperty.call(child.props, 'expanded') && !child.props.expanded) {
        clazz += ' graph-sizable';
        return React.cloneElement(child, { forwardRef: this.chartRef });
      }
      return child;
    });

    return (
      <div className={clazz} ref={this.thisRef} style={{ minHeight: this.state.minHeight }}>
        <header>
          <Heading />
          <div className="dropdown dload">
            <button
              className="btn btn-sm btn-outline-secondary"
              type="button"
              data-toggle="dropdown"
              aria-expanded="false"
              aria-haspopup="true"
            >
              <FontAwesomeIcon icon={['fas', 'download']} />
            </button>
            <div className="dropdown-menu dropdown-menu-right dload-menu">
              <button type="button" onClick={e => this.download(e)} className="dropdown-item">
                png
              </button>
              <button type="button" onClick={e => this.download(e)} className="dropdown-item">
                jpeg
              </button>
            </div>
          </div>
        </header>
        {childs}
        <ReactResizeDetector skipOnMount handleHeight handleWidth onResize={this.triggerResize} />
      </div>
    );
  }
}

GraphContainer.propTypes = {
  /** Title as a Link to */
  to: PropTypes.string,
  /** Title */
  title: PropTypes.string.isRequired,
  /** Contains any graph */
  children: PropTypes.node.isRequired,
};

GraphContainer.defaultProps = {
  to: undefined,
};

export default GraphContainer;
