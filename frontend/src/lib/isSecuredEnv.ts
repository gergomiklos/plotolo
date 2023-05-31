

export const isSecuredEnv = () => {
  return process.env.SECURE === 'true';
}