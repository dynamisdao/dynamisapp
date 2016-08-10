import Web3 from 'web3';

var web3cache = {};

function getWeb3(url) {
  if(web3cache[url]) {
    return web3cache[url];
  }
  var web3 = new Web3();
  web3.setProvider(new web3.providers.HttpProvider(url));
  web3cache[url] = web3;
  return web3;
}

export function getBalance(web3url, address, callback) {
  getWeb3(web3url).eth.getBalance(address, callback);
}

export function getTransactionCount(web3url, address, callback) {
  getWeb3(web3url).eth.getTransactionCount(address, callback);

}
export function sendRawTransaction(web3url, tx, callback) {
  getWeb3(web3url).eth.sendRawTransaction(tx, callback);

}
export function getTransactionReceipt(web3url, hash, callback) {
  getWeb3(web3url).eth.getTransactionReceipt(hash, callback);
}

export function getFirstBlockHash(web3url, callback) {
  getWeb3(web3url).eth.getBlock(0, callback);
}
