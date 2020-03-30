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
import { Route, Switch, BrowserRouter } from 'react-router-dom';
import Dashboard from './pages/dashboard';
import SearchPage from './pages/search';
import ScanPage from './pages/scan';
import InfoPage from './pages/info';
import ExportPage from './pages/export';
import PackagePage from './pages/package';
import ResultsPage from './pages/results';
import CVEPage from './pages/cve';
import Sidebar from './components/sidebar';
import './App.scss';
import Hamburger from './components/sidebar/hamburger';
import Imprint from './pages/Imprint/imprint';
import DSGVO from './pages/DSGVO';
import Footer from './components/footer';

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isOpen: true,
    };
    this.close = this.close.bind(this);
    this.open = this.open.bind(this);
  }

  componentDidMount() {
    window.addEventListener('resize', this.resize.bind(this));
    this.resize();
  }

  resize() {
    this.setState({ isOpen: window.innerWidth > 760 });
  }

  close() {
    this.setState({ isOpen: false });
  }

  open() {
    this.setState({ isOpen: true });
  }

  render() {
    return (
      <BrowserRouter>
        <Sidebar open={this.state.isOpen} click={this.close} />
        <Hamburger click={this.open} />
        <div className="h-100 d-flex flex-column">
          <main className={`pt-3 px-4 ${this.state.isOpen && 'open'}`}>
            <Switch>
              <Route exact path="/" component={Dashboard} />
              <Route path="/search" component={SearchPage} />
              <Route path="/package/:name" component={PackagePage} />
              <Route path="/scan" component={ScanPage} />
              <Route path="/results" component={ResultsPage} />
              <Route path="/info" component={InfoPage} />
              <Route path="/export" component={ExportPage} />
              <Route path="/cve/:id" component={CVEPage} />
              <Route path="/imprint" component={Imprint} />
              <Route path="/dsgvo" component={DSGVO} />
            </Switch>
          </main>
          <Footer className={`py-3 px-4 ${this.state.isOpen && 'open'}`} />
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
