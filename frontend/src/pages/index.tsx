import Link from "next/link";
import {ArrowUpTrayIcon, ChevronRightIcon} from '@heroicons/react/20/solid'
import {FlagIcon} from "@heroicons/react/24/solid";
import {ArrowRightOnRectangleIcon, CheckCircleIcon, Cog6ToothIcon, TrashIcon} from "@heroicons/react/24/outline";
import React, {useState} from "react";
import {getServerSession} from "next-auth/next";
import {authOptions} from "@/pages/api/auth/[...nextauth]";
import {GetServerSidePropsContext} from "next";
import {User} from "next-auth";
import {signOut} from "next-auth/react";
import {isSecuredEnv} from "@/lib/isSecuredEnv";
import {App} from "@/types";
import NotebookUpload from "@/components/notebookUpload";


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

  const res = await fetch('http://localhost:8088/apps');
  const apps = (await res.json()).apps || [];

  //@ts-ignore
  return {props: {apps, user: session?.user || null}};
}


export default function Home({apps, user}: {apps: App[], user: User}) {
  const [isEditing, setIsEditing] = useState(false);

  return (
    <main className="flex flex-row justify-center min-h-screen bg-gray-50 text-gray-900">

      <div className="absolute top-1 right-1 p-1 flex gap-x-3">
        {user?.name && <div className="text-gray-500">
          {user.name}
        </div>}
        <Cog6ToothIcon
          className="h-6 w-6 cursor-pointer text-gray-500 hover:text-gray-900"
          onClick={() => setIsEditing(!isEditing)}
        />
        {user && <ArrowRightOnRectangleIcon
          className="h-6 w-6 cursor-pointer text-gray-500 hover:text-gray-900"
          onClick={() => signOut()}
        />}
      </div>

      <div className="w-full max-w-4xl p-5">
        <h1 className="text-3xl font-bold mb-10">
          <FlagIcon className="h-7 w-7 inline-block text-red-500 mr-2 pb-1"/>
          Plotolo
        </h1>

        {isEditing && <NotebookUpload/>}

        <div className="divide-y divide-gray-100 border-gray-50 border-2 max-w-4xl rounded-xl bg-white overflow-hidden">
          {apps.map((app) => (
            <div className="" key={app.id}>
              <AppListElement app={app} isEditing={isEditing}/>
            </div>
          ))}
        </div>
      </div>
    </main>
  )
}


const AppListElement = ({app, isEditing}) => {
  const [waiting, setWaiting] = useState(false);

  const onDelete = async () => {
    try {
      setWaiting(true);

      const response = await fetch(`/server/scripts/${app.id}`, {
        method: 'DELETE',
        credentials: 'include',
      });

      setWaiting(false);

      if (response.ok) {
        // fetchApps();
      } else {
        alert('Error while deleting app.');
      }
    } catch (e) {
      console.error(e);
      alert('Error while deleting app.');
      setWaiting(false);
    }
  };

  return (
    <LinkWrapper href={isEditing ? '#' : `/app/${app.id}?back=true`} key={app.id}>
      <div className="p-5 hover:bg-gradient-to-r from-gray-100 to-white flex justify-between">
        <div className="text-lg">
          {app.name}
        </div>
        {isEditing && <TrashIcon className="h-8 w-8 text-red-400 hover:bg-red-50 rounded-full p-2 cursor-pointer"
                                 onClick={onDelete}/>}
        {!isEditing && <ChevronRightIcon className="h-5 w-5 text-gray-400"/>}
      </div>
    </LinkWrapper>
  )
}


const LinkWrapper = ({href, children, ...props}) => {
  if (href == "#") {
    return (<>{children}</>);
  }
  return (
    <Link href={href} {...props} >
      {children}
    </Link>
  );
};
