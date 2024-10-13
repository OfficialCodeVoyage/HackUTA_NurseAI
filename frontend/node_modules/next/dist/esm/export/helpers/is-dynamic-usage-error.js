import { isDynamicServerError } from '../../client/components/hooks-server-context';
import { isBailoutToCSRError } from '../../shared/lib/lazy-dynamic/bailout-to-csr';
import { isNextRouterError } from '../../client/components/is-next-router-error';
export const isDynamicUsageError = (err)=>isDynamicServerError(err) || isBailoutToCSRError(err) || isNextRouterError(err);

//# sourceMappingURL=is-dynamic-usage-error.js.map