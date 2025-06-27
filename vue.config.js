const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      // 代理所有以 `/api` 开头的请求
      '/api': {
        target: 'http://localhost:5000', // 后端服务器地址
        changeOrigin: true, // 改变请求头中的 Host 为目标地址
        pathRewrite: {
          '^/api': '', // 去掉路径中的 `/api` 前缀
        },
      },
      // 如果你有多个后端接口，可以继续添加其他代理规则
      // '/auth': {
      //   target: 'http://localhost:5001',
      //   changeOrigin: true,
      //   pathRewrite: { '^/auth': '' },
      // },
    },
  },
})