/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-bziyhi8qwaekwd3z.us', // the auth0 domain prefix
    audience: 'image', // the audience set for the auth0 app
    clientId: 'DVhndO3e5HWlKqD6rzDu6dmGsUayXrT0', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application.
  }
};
