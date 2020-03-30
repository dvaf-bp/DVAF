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
import PageTitle from '../../components/pagetitle';
import './upload.scss';
import { BASE_URL } from '../../constants';
import example from './example';

class Upload extends Component {
  constructor(props) {
    super(props);

    this.state = {
      onDropzone: false,
      dropzoneText: 'Drag here or choose a file',
      isLoading: false,
      textArea: '',
    };

    this.dragOver = this.dragOver.bind(this);
    this.dragLeave = this.dragLeave.bind(this);
    this.dragDrop = this.dragDrop.bind(this);
    this.fileChange = this.fileChange.bind(this);
    this.checkTextArea = this.checkTextArea.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.uploadExample = this.uploadExample.bind(this);
  }

  dragOver(e) {
    e.stopPropagation();
    e.preventDefault();
    this.setState({ onDropzone: true });
  }

  dragLeave() {
    this.setState({ onDropzone: false });
  }

  dragDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    this.checkFile(e.dataTransfer.files);
  }

  fileChange(e) {
    this.checkFile(e.target.files);
  }

  checkFile(droppedFiles) {
    if (droppedFiles.length > 1) {
      this.setState({ dropzoneText: 'Please upload one file at a time' });
      return;
    }
    if (droppedFiles.length === 0) return;
    if (droppedFiles[0].type !== 'text/plain') {
      this.setState({ dropzoneText: 'File is not of type text/plain!' });
      return;
    }

    this.setState(
      {
        dropzoneText: `Analyzing ${droppedFiles[0].name}...`,
        isLoading: true,
      },
      () => {
        droppedFiles[0].text().then(text => {
          this.uploadText(text);
        });
      },
    );
  }

  uploadExample() {
    this.setState(
      {
        dropzoneText: `Analyzing...`,
        isLoading: true,
      },
      this.uploadText(example),
    );
  }

  checkTextArea(e) {
    e.preventDefault();
    e.stopPropagation();

    this.setState(
      {
        dropzoneText: `Analyzing...`,
        isLoading: true,
      },
      this.uploadText(this.state.textArea),
    );
  }

  uploadText(text) {
    const packages = text.split(/\r?\n/).filter(n => n);

    fetch(`${BASE_URL}/api/v1/packages/upload`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        packages,
      }),
    })
      .then(response => response.json())
      .then(data => {
        this.props.history.push({
          pathname: '/results',
          cves: data.packages,
          polar_chart: data.polar_chart,
        });
      })
      .catch(e => console.error(e));
  }

  handleChange(event) {
    this.setState({ textArea: event.target.value });
  }

  render() {
    const loader = (
      <div className="d-flex align-items-center justify-content-center my-5">
        <div className="spinner-border" role="status" aria-hidden="true" />
        <h3 className="ml-2 mb-0">{this.state.dropzoneText}</h3>
      </div>
    );

    const uploader = (
      <>
        <div className="uploader">
          <ul className="nav nav-tabs">
            <li className="nav-item active">
              <a className="nav-link active" href="#filetab" data-toggle="tab">
                Upload File
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#inputtab" data-toggle="tab">
                Upload Text
              </a>
            </li>
          </ul>
          <div className="tab-content mb-4">
            <div id="filetab" className="tab-pane fade in show active">
              <form
                draggable="true"
                action=""
                className={`dropzone ${this.state.onDropzone && 'is-dragover'}`}
                onDragOver={this.dragOver}
                onDragEnter={this.dragOver}
                onDragLeave={this.dragLeave}
                onDragEnd={this.dragLeave}
                onDrop={e => {
                  this.dragLeave();
                  this.dragDrop(e);
                }}
                onChange={this.fileChange}
                encType="multipart/form-data"
              >
                <div className="dropzone-input">
                  <FontAwesomeIcon icon={['fas', 'file-upload']} className="ico" />
                  <label htmlFor="file">
                    <input className="dropzone-file" type="file" name="file" id="file" />
                  </label>
                  <span>{this.state.dropzoneText}</span>
                </div>
              </form>
            </div>
            <div id="inputtab" className="tab-pane fade">
              <form action="" className="direct-input" encType="multipart/form-data">
                <textarea type="text" name="input" id="input" value={this.state.textArea} onChange={this.handleChange} required />
                <button className="btn btn-primary" type="submit" onClick={this.checkTextArea}>
                  Submit
                </button>
              </form>
            </div>
          </div>
        </div>
        <p>
          You can also use our example package list. Just click{' '}
          <button type="button" className="btn btn-primary" onClick={this.uploadExample}>
            here!
          </button>
        </p>
      </>
    );

    return (
      <>
        <PageTitle>Upload</PageTitle>
        <p>
          Upload a list of packages and get back a detailed report. Use a plain text document and put each package in a separate line. You
          can also upload the output of apt directly.
        </p>
        {this.state.isLoading ? loader : uploader}
        <p>
          <strong>Hint:</strong> You can export all installed packages including the ones shipped with debian by default using{' '}
          <code>apt list --installed | tail -n +2 &gt; apt_installed.txt</code>. If you are just interested in the ones you have installed
          explicitly, use <code>apt list --manual-installed | tail -n +2 &gt; apt_installed.txt</code>.
        </p>
      </>
    );
  }
}

Upload.propTypes = {
  history: PropTypes.shape({
    push: PropTypes.func.isRequired,
  }).isRequired,
};

export default Upload;
