import { ReactNode } from 'react';

interface Props {
  className?: string;
  children: ReactNode;
}

export default function LoadingSpinner({ className = '', children }: Props) {
  return (
    <div className={`flex flex-col items-center justify-center py-12 ${className}`}>
      <div className="w-10 h-10 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin" />
      {children && <p className="mt-4 text-gray-500 dark:text-gray-400">{children}</p>}
    </div>
  );
}
