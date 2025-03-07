module.exports = {
  apps: [
    {
      name: 'API',
      script: 'index.js',
      instances: 1,
      autorestart: true,
      watch: true,
      ignore_watch: ['pids', 'logs', 'node_modules', '.git', '.git/index.lock'],
      max_memory_restart: '1G',
      env: {
        PORT: 3000,
        NODE_ENV: 'development',
      },
      env_production: {
        PORT: 3000,
        NODE_ENV: 'production',
      },
    },
  ],
};
