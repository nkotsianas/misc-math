function y = asinc( x, acc )
% Returns the inverse of the sinc function (defined: sinc(x) = sin(x)/x,
%   x: [~ -.217,1], sinc(x): [~ 4.5,0]), by interpolating the values of
%   sinc. Samples are taken with spacing "acc", which is .001 by default.
%   "x" can be a scalar or array.
% Results accuracy:
%   max(abs(sinc(asinc(x)/pi)-x)) = 3.918878388464719e-09
%   std(sinc(asinc(x)/pi)-x) = 3.551989089220288e-11
% (Note that MATLAB defines sinc(x) = sin(pi*x)/(pi*x).)

if nargin < 2
    acc = .001;
end

ys = 0:acc:4.4934094579;
xs = sinc(ys/pi); %

y = interp1(xs,ys,x,'spline');



end

