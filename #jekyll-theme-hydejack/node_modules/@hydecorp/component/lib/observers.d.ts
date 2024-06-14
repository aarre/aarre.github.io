import { Observable } from "rxjs";
export declare function createResizeObservable(el: HTMLElement): Observable<ResizeObserverEntry>;
export declare function createMutationObservable(el: HTMLElement, options?: MutationObserverInit): Observable<MutationRecord>;
export declare function createIntersectionObservable(els: HTMLElement | HTMLElement[], options?: IntersectionObserverInit): Observable<IntersectionObserverEntry[]>;
//# sourceMappingURL=observers.d.ts.map