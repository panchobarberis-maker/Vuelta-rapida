const https = require('https');
const fs = require('fs');
const path = require('path');

const MARCAS = {
  vueltarapida: {
    nombre: 'Vuelta Rápida Store',
    facebook: {
      pageId: '1714180835332024',
      token: 'EAAY3dylw6wgBRt9DhonN4sAXXW2ZCKBapJZBQcUZC94Hvr1yHsLHQ4mCgeKrZBuCY3AUYVoTGIL3anHAV0MgAhnn770MlQVHSzjvjuEvDs4vgUTbgbKI8ZAnbCn9EJPlMa9LCKqc9JZCSkd802xQOYucO3xsinGZC9ZAJk8Ec7r8dN3e4n5JfwxW4fq2vew4dzZCYWKgvDFwV',
    },
    instagram: {
      accountId: '17841463191318516',
    },
  },
  clickderecho: {
    nombre: 'Click Derecho MKT',
    facebook: {
      pageId: '998980863296015',
      token: 'EAAY3dylw6wgBRg0JlexPrPn13pdNZCjXPJbFMImPZBwQdNvkuw358ARTw5yBEkWW7B6TzFT1xEWsNVhyHFRKLX4N0ymnebuUtm3DyunaPDfBFMOu1xRPFj93mDZCzL5U25QC0ZCi6CUZA331xhMVZCER6rbYSmQpnaoe76FlKswVew5PIeFJDTIApEzuN4WkFn3gGZANbMZC',
    },
    instagram: {
      accountId: '17841480248184525',
    },
  },
};

function request(options, body) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => resolve(JSON.parse(data)));
    });
    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

async function postearFacebook(marca, imagenUrl, caption) {
  const { pageId, token } = marca.facebook;
  const body = `url=${encodeURIComponent(imagenUrl)}&caption=${encodeURIComponent(caption)}&access_token=${token}`;
  const res = await request({
    hostname: 'graph.facebook.com',
    path: `/v25.0/${pageId}/photos`,
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Content-Length': Buffer.byteLength(body),
    },
  }, body);
  return res;
}

async function postearInstagram(marca, imagenUrl, caption) {
  const { accountId } = marca.instagram;
  const token = marca.facebook.token;

  // Paso 1: crear container
  const bodyContainer = `image_url=${encodeURIComponent(imagenUrl)}&caption=${encodeURIComponent(caption)}&access_token=${token}`;
  const container = await request({
    hostname: 'graph.facebook.com',
    path: `/v25.0/${accountId}/media`,
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Content-Length': Buffer.byteLength(bodyContainer),
    },
  }, bodyContainer);

  if (!container.id) {
    return { error: 'No se pudo crear el container', detalle: container };
  }

  // Paso 2: publicar
  const bodyPublish = `creation_id=${container.id}&access_token=${token}`;
  const resultado = await request({
    hostname: 'graph.facebook.com',
    path: `/v25.0/${accountId}/media_publish`,
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Content-Length': Buffer.byteLength(bodyPublish),
    },
  }, bodyPublish);

  return resultado;
}

async function postear(marcaKey, imagenUrl, caption) {
  const marca = MARCAS[marcaKey];
  if (!marca) {
    console.log('Marca no encontrada. Usá: vueltarapida o clickderecho');
    return;
  }

  console.log(`\nPublicando en ${marca.nombre}...`);

  const [fb, ig] = await Promise.all([
    postearFacebook(marca, imagenUrl, caption),
    postearInstagram(marca, imagenUrl, caption),
  ]);

  console.log('Facebook:', fb);
  console.log('Instagram:', ig);
}

// Argumentos: node postear.js <marca> <url-imagen> <caption>
const [,, marcaKey, imagenUrl, ...captionParts] = process.argv;
const caption = captionParts.join(' ');

if (!marcaKey || !imagenUrl || !caption) {
  console.log('Uso: node postear.js <marca> <url-imagen> <caption>');
  console.log('Marcas disponibles: vueltarapida, clickderecho');
  console.log('Ejemplo: node postear.js vueltarapida https://... "Nuevo producto!"');
  process.exit(1);
}

postear(marcaKey, imagenUrl, caption);
