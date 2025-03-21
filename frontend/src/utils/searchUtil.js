export function matchQuery(str, query) {
  if (!str) return false;
  return str.toLowerCase().includes(query.toLowerCase());
}
