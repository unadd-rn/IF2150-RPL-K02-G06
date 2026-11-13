import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const role = request.cookies.get('role')?.value;
  const path = request.nextUrl.pathname;

  if (path.startsWith('/penjual') && role !== 'PENJUAL') {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  if (path.startsWith('/katalog') && role !== 'PEMBELI') {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/penjual/:path*', '/katalog/:path*'],
};