import store from '@/store';

export async function fetchHelper(method, apiPath, payload = null) {
  const options = {
    method,
    credentials: 'include',
    headers: {},
  };

  if (payload) {
    options.headers['Content-Type'] = 'application/json';
    options.body = JSON.stringify(payload);
  }

  try {
    const response = await fetch(`${store.api.origin}${apiPath}`, options);
    const data = await response.json();
    return { ok: response.ok, status: response.status, data };
  } catch (error) {
    console.error('Fetch error:', error);
    throw error;
  }
}

export async function get(apiPath) {
  const { data, status } = await fetchHelper('GET', apiPath);
  console.log('GET', apiPath, status, data);
  return data;
}

export async function post(apiPath, payload = {}) {
  const { data, status } = await fetchHelper('POST', apiPath, payload);
  console.log('POST', apiPath, status, data);
  return data;
}

export async function put(apiPath, payload = {}) {
  const { data, status } = await fetchHelper('PUT', apiPath, payload);
  console.log('PUT', apiPath, status, data);
  return data;
}

export async function del(apiPath) {
  const { data, status } = await fetchHelper('DELETE', apiPath);
  console.log('DELETE', apiPath, status, data);
  return data;
}
