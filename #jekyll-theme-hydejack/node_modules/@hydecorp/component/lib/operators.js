import { NEVER } from "rxjs";
import { filter, map, switchMap, withLatestFrom, tap, debounceTime } from "rxjs/operators";
export function subscribeWhen(p$) {
    return (source) => {
        return p$.pipe(switchMap(p => (p ? source : NEVER)));
    };
}
export function unsubscribeWhen(p$) {
    return (source) => {
        return p$.pipe(switchMap(p => (p ? NEVER : source)));
    };
}
// export function filterWhen<T>(p$: Observable<boolean>) {
//   return (source: Observable<T>) => {
//     return source.pipe(
//       withLatestFrom(p$),
//       filter(([, p]) => p),
//       map(([x]) => x)
//     );
//   };
// };
export function filterWhen(p$, ...others) {
    return (source) => {
        if (others.length === 0) {
            return source.pipe(withLatestFrom(p$), filter(([, p]) => p), map(([x]) => x));
        }
        return source.pipe(withLatestFrom(p$, ...others), filter(([, ...ps]) => ps.every(p => p)), map(([x]) => x));
    };
}
;
export function bufferDebounceTime(time = 0) {
    return (source) => {
        let bufferedValues = [];
        return source.pipe(tap(value => bufferedValues.push(value)), debounceTime(time), map(() => bufferedValues), tap(() => bufferedValues = []));
    };
}
//# sourceMappingURL=operators.js.map