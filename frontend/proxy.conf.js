const rewriteCookies = (proxyRes, req, res) => {
  const host = req.hostname;

  let cookies = proxyRes.headers['set-cookie'];
  if (!cookies) { return; }
  if (typeof cookies === 'string') { cookies = [cookies]; }

  cookies = cookies.map(cookie => {
    return cookie
      .replace(/(; Domain)=?[^;]*/ig, `$1=${host}`)
      .replace(/; Secure=?[^;]*/ig, '');
  });

  proxyRes.headers['set-cookie'] = cookies;
}


const PROXY_CONFIG = {
  '/api/*': {
    target: 'http://127.0.0.1:5000',
    secure: false,
    changeOrigin: true,
    logLevel: 'debug',
    onProxyRes: rewriteCookies
  }
};

module.exports = PROXY_CONFIG;
