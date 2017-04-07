function it = mandelbrot_time(z0, p, c, N, dv)
% Computes the number of iterations of the fractal sequence
%   z(k+1) = z(k)^p + c before it diverges.
% Condition for divergence is abs(z(k)) > 2.
%   - z0: starting value.
%   - p: power on z
%   - c: constant in the iteration.
%   - N: maximum number of iterations (default = 100).
%   - dv: print out progress statements every dv percent during execution.
%      0 = don't print anything. (default = 0).
%
% Dependencies:
%   - None.


% ----------------------- %
% set some defaults
if nargin <= 4
    dv = 0;
    if nargin == 3
        N = 100;
    end
end
% ----------------------- %

z = z0*ones(size(c));
it = ones(size(c));

for k=2:N
    znew = z.^p + c;
    znew(abs(znew) > 2) = Inf;
    it(~isinf(znew)) = it(~isinf(znew)) + 1;
    if dv > 0 && any(k == ceil((dv:dv:100)*N/100))
        fprintf('%.f%% Completed\n', 100*k/N);
    end
    z = znew;
end

end


