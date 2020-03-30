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
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import Spinner from 'react-bootstrap/Spinner';
import { BASE_URL } from '../../constants';
import PackageEntry from './PackageEntry';
import CVEEntry from './CVEEntry';

/**
 * Search component
 */
class Searcher extends Component {
  constructor(props) {
    super(props);

    this.state = {
      query: '',
      results: [],
      show: 10,
      loading: false,
      message: '',
    };

    this.timeout = null;
    this.search = this.search.bind(this);
  }

  componentDidMount() {
    window.addEventListener('scroll', () => {
      if (window.innerHeight + window.scrollY >= document.body.scrollHeight - 100) {
        this.setState(prev => ({
          show: prev.show + 10,
        }));
      }
    });

    const params = new URLSearchParams(window.location.search);
    const query = params.get('query') || '';
    if (query !== '') this.setState({ query }, this.query);
  }

  /**
   * Sets the URL to represent the current query
   * @param {string} query query
   */
  setParams(query) {
    const searchParams = new URLSearchParams();
    searchParams.set('query', query);
    this.props.history.push(`?${searchParams.toString()}`);
  }

  /**
   * Updates the input of the search bar
   * @param {*} e typing event
   */
  search(e) {
    clearTimeout(this.timeout);

    this.setState({ query: e.target.value }, this.query);
  }

  /**
   * Queries the backend after 250ms of no typing
   */
  query() {
    this.timeout = setTimeout(() => {
      const value = this.state.query;

      this.setParams(value);

      if (value === '') {
        this.setState({ results: [] });
        return;
      }
      if (value.length < 3) {
        this.setState({ message: 'you have to enter more then 3 charakters to start searching...', loading: false, results: [] });
        return;
      }

      this.setState({ message: '', loading: true });

      if (value.substr(0, 3).toLowerCase() !== 'cve') {
        fetch(`${BASE_URL}/api/v1/packages/match/${value}`)
          .then(response => response.json())
          .then(data => {
            this.setState({ results: data, loading: false });
          })
          .catch(err => console.error(err));
      } else {
        fetch(`${BASE_URL}/api/v1/cves/match/${value.toUpperCase()}`)
          .then(response => response.json())
          .then(data => {
            this.setState({
              results: data.cves,
              loading: false,
            });
          })
          .catch(err => console.error(err));
      }
    }, 250);
  }

  render() {
    return (
      <>
        <div className="input-group mb-2">
          <div className="input-group-prepend">
            <div className="input-group-text">
              <FontAwesomeIcon icon={faSearch} />
            </div>
          </div>
          <input
            type="text"
            className="form-control form-control-lg"
            placeholder="Search for package or cve..."
            value={this.state.query}
            onChange={this.search}
          />
        </div>
        <h2 className="pt-3">Results</h2>
        <div className="container-fluid">
          {this.state.message}
          {this.state.loading ? (
            <div style={{ textAlign: 'center' }}>
              <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
            </div>
          ) : (
            this.state.results.slice(0, this.state.show).map(result => {
              if (this.state.query === '') return '';

              return this.state.query.substr(0, 3).toLowerCase() === 'cve' ? (
                <CVEEntry name={result.id} query={this.state.query} cvss={result.cvss ? result.cvss : 0} desc="" />
              ) : (
                <PackageEntry
                  name={result.name}
                  query={this.state.query}
                  description={result.description}
                  aliases={result.aliases}
                  cvss={result.highest_affecting_cvss}
                />
              );
            })
          )}
        </div>
      </>
    );
  }
}

Searcher.propTypes = {
  /** history object to set the query in url */
  history: PropTypes.shape({ push: PropTypes.func.isRequired }).isRequired,
};

export default Searcher;
