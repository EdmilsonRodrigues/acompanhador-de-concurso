import { HttpEvent, HttpInterceptorFn, HttpResponse } from '@angular/common/http';
import { map } from 'rxjs';

export const convertCaseInterceptor: HttpInterceptorFn = (req, next) => {
  if (req.body && typeof req.body === 'object' && !(req.body instanceof FormData)) {
    const transformedBody = camelToSnakeCase(req.body);
    req = req.clone({ body: transformedBody });
  }

  return next(req).pipe(
    map((event: HttpEvent<any>) => {
      if (event instanceof HttpResponse && event.body) {
        const transformedBody = snakeToCamelCase(event.body);
        return event.clone({ body: transformedBody });
      }
      return event
    })
  );
};


function camelToSnakeCase(obj: any): any {
  const convert = (key: string) => key.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`);
  return convertCase(obj, convert);
}

function snakeToCamelCase(obj: any): any {
  const convert = (key: string) => key.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
  return convertCase(obj, convert);
}

function convertCase(obj: any, convert: (obj: string) => string): any {
  if (Array.isArray(obj)) {
    return obj.map((o) => convertCase(o, convert));
  }
  if (obj && typeof obj === 'object') {
    const result: any = {};
    for (const key in obj) {
      if (Object.prototype.hasOwnProperty.call(obj, key)) {
        result[convert(key)] = convertCase(obj[key], convert);
      }
    }
    return result;
  }
  return obj;
}
