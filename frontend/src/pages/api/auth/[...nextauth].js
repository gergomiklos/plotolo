import NextAuth from "next-auth"
import GithubProvider from "next-auth/providers/github"
import GitlabProvider from "next-auth/providers/gitlab";
import GoogleProvider from "next-auth/providers/google";
import AzureADProvider from "next-auth/providers/azure-ad"
import CognitoProvider from "next-auth/providers/cognito";
import OktaProvider from "next-auth/providers/okta";
import OneLoginProvider from "next-auth/providers/onelogin";
import KeycloakProvider from "next-auth/providers/keycloak";
import OAuthConfig from "next-auth/providers/auth0";


const getProviderConfig = () => {
  const providers = [];
  if(process.env.GITHUB_ID){
    providers.push(GithubProvider({
      clientId: process.env.GITHUB_ID,
      clientSecret: process.env.GITHUB_SECRET,
    }));
  }
  if(process.env.GITLAB_ID){
    providers.push(GitlabProvider({
      clientId: process.env.GITLAB_ID,
      clientSecret: process.env.GITLAB_SECRET,
    }));
  }
  if(process.env.GOOGLE_ID){
    providers.push(GoogleProvider({
      clientId: process.env.GOOGLE_ID,
      clientSecret: process.env.GOOGLE_SECRET,
    }));
  }
  if(process.env.AZURE_AD_ID){
    providers.push(AzureADProvider({
      clientId: process.env.AZURE_AD_ID,
      clientSecret: process.env.AZURE_AD_SECRET,
      tenantId: process.env.AZURE_AD_TENANT_ID,
    }));
  }
  if(process.env.COGNITO_ID){
    providers.push(CognitoProvider({
      clientId: process.env.COGNITO_ID,
      clientSecret: process.env.COGNITO_SECRET,
      issuer: process.env.COGNITO_ISSUER,
    }));
  }
  if(process.env.OKTA_ID){
    providers.push(OktaProvider({
      clientId: process.env.OKTA_ID,
      clientSecret: process.env.OKTA_SECRET,
    }));
  }
  if(process.env.ONELOGIN_ID){
    providers.push(OneLoginProvider({
      clientId: process.env.ONELOGIN_ID,
      clientSecret: process.env.ONELOGIN_SECRET,
    }));
  }
  if(process.env.KEYCLOAK_ID){
    providers.push(KeycloakProvider({
      clientId: process.env.KEYCLOAK_ID,
      clientSecret: process.env.KEYCLOAK_SECRET,
      issuer: process.env.KEYCLOAK_ISSUER,
    }));
  }
  if(process.env.OAUTH_ID){
    providers.push(OAuthConfig({
      clientId: process.env.OAUTH_ID,
      clientSecret: process.env.OAUTH_SECRET,
    }));
  }
  return providers;
}


export const authOptions = {
  // Configure one or more authentication providers
  providers: getProviderConfig(),
  session: {
    jwt: true,
  },
}

export default NextAuth(authOptions)