export var MockKeyBaseService = {
  lookupUser(username) {
    var mockData = {
      pipermerriam: {
        username: 'pipermerriam',
        twitter: 'pipermerriam',
      }
    };
    return new Promise(function(resolve, reject) {
      if(mockData[username]) {
        resolve(mockData[username]);
      }
      reject({
        code: 205,
        desc: username + ': user not found',
        name: 'NOT_FOUND'
      });
    });
  },
};
