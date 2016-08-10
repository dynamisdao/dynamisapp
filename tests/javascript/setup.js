var jsdom = require('jsdom');

global.document = jsdom.jsdom('<!doctype html><html><body></body></html>');
global.window = global.document.defaultView;
global.navigator = global.window.navigator;
global.TestUtils = require('./test-utils');
global.TestMocks = require('./mocks');
global.Materialize = {
  updateTextFields() {}
};
