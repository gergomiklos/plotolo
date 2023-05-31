import {signIn, getProviders} from "next-auth/react"
import React, {useEffect, useState} from "react";
import {Provider} from "next-auth/providers";
import {FlagIcon} from "@heroicons/react/24/solid";
import {ChevronRightIcon} from "@heroicons/react/20/solid";
import {getServerSession} from "next-auth/next";
import {authOptions} from "@/pages/api/auth/[...nextauth]";


export const getServerSideProps = async (context) => {
  // const providers = await getProviders(); issue, does not work
  // @ts-ignore
  const session = await getServerSession(context.req, context.res, authOptions);

  if (!!session) {
    return {
      redirect: {
        destination: '/',
        permanent: false,
      },
    };
  }

  return {props: {}};
}


export default function LoginPage({}) {
  const [providers, setProviders] = useState<Provider[]>([]);

  useEffect(() => {
    (async () => {
      const providers = await getProviders();
      // @ts-ignore
      setProviders(Object.values(providers));
    })();
  }, []);

  return (
    <main className="flex flex-row justify-center min-h-screen bg-gray-50 text-gray-900">
      <div className="w-full max-w-2xl p-5">
        <h1 className="text-3xl font-bold mb-10">
          <FlagIcon className="h-7 w-7 inline-block text-red-500 mr-2 pb-1"/>
          Plotolo
        </h1>
        <div className="divide-y divide-gray-100 border-gray-50 border-2 max-w-4xl rounded-xl bg-white overflow-hidden">
          {providers.map((provider) => (
            <button
              key={provider.name}
              onClick={() => signIn(provider.id)}
              className="p-5 block w-full h-full hover:bg-gradient-to-r from-gray-100 to-white flex justify-between"
            >
              <div>
                Sign in with {provider.name}
              </div>
              <ChevronRightIcon className="h-5 w-5 text-gray-400"/>
            </button>
          ))}
        </div>
      </div>
    </main>
  )
}