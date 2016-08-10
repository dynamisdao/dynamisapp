export function setOn(reducer, key, value) {
  var action = { type: `SET.${reducer}.${key}`};
  action[key] = value;
  return action;
}
