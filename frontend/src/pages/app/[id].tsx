import React from 'react'
import {useRouter} from "next/router";
import {ArrowLeftIcon} from "@heroicons/react/24/outline";
import {ExclamationCircleIcon, HeartIcon} from "@heroicons/react/20/solid";
import {FlagIcon} from "@heroicons/react/24/solid"
import {getServerSession} from "next-auth/next";
import Head from 'next/head'
import {isSecuredEnv} from "@/lib/isSecuredEnv";
import {authOptions} from "@/pages/api/auth/[...nextauth]";
import useAppSession from "@/lib/usaAppSession";
import WebWidget from "@/components/webWidget";
import {GetServerSidePropsContext} from "next";


export const getServerSideProps = async (context: GetServerSidePropsContext) => {
  // @ts-ignore
  const session = await getServerSession(context.req, context.res, authOptions);

  if (!session && isSecuredEnv()) {
    return {
      redirect: {
        destination: '/login',
        permanent: false,
      },
    };
  }

  // @ts-ignore
  const { id: appId } = context.params;
  const res = await fetch(`http://localhost:8088/apps/${appId}`);
  const app = (await res.json()) || {};

  return {props: {app, user: session?.user || null}};
}

export default function App({ app }) {
  const router = useRouter();
  // @ts-ignore
  const {widgets, scriptState, addInputRequest} = useAppSession(app.id);

  return (
    <main className="flex flex-col items-center justify-between min-h-screen bg-gray-50 p-1 sm:px-5 sm:pt-10">
      <Head>
        <title>{app.name}</title>
      </Head>
      <div className="w-full min-h-2/3 max-w-4xl p-5 sm:p-10 bg-white rounded-2xl shadow-sm">
        <Navigation router={router}/>
        <div className="absolute top-1 right-1">
          {scriptState.errors.length > 0 &&
            <ExclamationCircleIcon className="h-5 w-5 text-red-300" aria-hidden="true"/>}
          {scriptState.status === 'RUNNING' &&
            <HeartIcon className="h-5 w-5 text-gray-500 animate-pulse" aria-hidden="true"/>}
        </div>

        <div className="">
          {widgets.filter(widget => widget.status !== 'DELETED').map((widget) => (
            <div className="p-3" key={widget.id}>
              <WebWidget
                widget={widget}
                onInput={addInputRequest}
                scriptStatus={scriptState.status}
              />
            </div>
          ))}
        </div>
      </div>

      <footer className="text-xs font-bold pt-5 text-center w-full">
        <a href={'https://www.plotolo.com'} className="opacity-50 hover:opacity-100">
          <FlagIcon className="h-4 w-4 inline-block text-red-500 mr-1 pb-1"/>
          Plotolo
        </a>
      </footer>
    </main>
  )
}


const Navigation = ({router}) => {
  let {back} = router.query;

  return (
    <div className="absolute top-2 left-2">
      {back === 'true' &&
        <ArrowLeftIcon
          onClick={() => router.push('/')}
          className="h-5 w-5 sm:h-6 sm:w-6 text-gray-500 hover:text-gray-900 cursor-pointer" aria-hidden="true"
        />
      }
    </div>
  )
}