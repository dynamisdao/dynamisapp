// eslint-disable-next-line no-undef
module.exports.config = {
  // See http://brunch.io/#documentation for docs.
  files: {
    javascripts: {
      joinTo: 'js/app.js'
    },
    stylesheets: {
      joinTo: 'css/app.css'
    },
  },

  paths: {
    watched: [
      'dynamis/static/js',
      'dynamis/static/css',
      'dynamis/static/vendor',
      'dynamis/static/schema',
    ],
    public: 'public/compiled'
  },

  // Note that this Babel config needs to match `.babelrc` so that Mocha
  // mirrors the same build pipeline.
  plugins: {
    babel: {
      presets: ['es2015-without-strict', 'react'],
      plugins: ['transform-object-rest-spread']
    },
    assetsmanager: {
      copyTo: {
        'fonts': ['node_modules/materialize-css/fonts/*'],
        'js': [
          'node_modules/materialize-css/dist/js/materialize.js',
        ],
      }
    }
  },

  modules: {
    autoRequire: {
      'js/app.js': ['dynamis/static/js/init']
    }
  },

  conventions: {
    assets: /^(dynamis\/static\/vendor)/,
    ignored: /\.test\.js/
  },

  npm: {
    enabled: true,
    styles: {
      'materialize-css': ['dist/css/materialize.css']
    },
    globals: {
      '$': 'jquery',
      'ReactDOM': 'react-dom',
      'React': 'react',
    }
  }
};
