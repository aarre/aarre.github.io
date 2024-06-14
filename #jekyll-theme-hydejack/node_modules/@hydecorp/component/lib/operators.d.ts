import { Observable, OperatorFunction } from "rxjs";
export declare function subscribeWhen<T>(p$: Observable<boolean>): (source: Observable<T>) => Observable<T>;
export declare function unsubscribeWhen<T>(p$: Observable<boolean>): (source: Observable<T>) => Observable<T>;
export declare function filterWhen<T>(p$: Observable<boolean>, ...others: Observable<boolean>[]): (source: Observable<T>) => Observable<T>;
export declare function bufferDebounceTime<T>(time?: number): OperatorFunction<T, T[]>;
//# sourceMappingURL=operators.d.ts.map