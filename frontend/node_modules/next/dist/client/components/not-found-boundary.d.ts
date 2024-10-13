import React from 'react';
interface NotFoundBoundaryProps {
    notFound?: React.ReactNode;
    notFoundStyles?: React.ReactNode;
    asNotFound?: boolean;
    children: React.ReactNode;
    missingSlots?: Set<string>;
}
export declare function NotFoundBoundary({ notFound, notFoundStyles, asNotFound, children, }: NotFoundBoundaryProps): import("react/jsx-runtime").JSX.Element;
export {};
