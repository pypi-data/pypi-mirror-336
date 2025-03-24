function s2let_hpx_write_real_spin_maps(fQ, fU, filename)

% s2let_hpx_rite_real_spin_maps 
% Write a real Healpix map to a FITS file
% Default usage :
%
%   s2let_hpx_write_real_spin_maps(fQ, fU, file)
%
% f the Healpix map to be written,
% file the name of the output FITS file.
%
% S2LET package to perform Wavelets transform on the Sphere.
% Copyright (C) 2012-2015  Boris Leistedt & Jason McEwen
% See LICENSE.txt for license details

sz = size(fQ);
szb = max([sz(1), sz(2)]);
nside = floor(sqrt(szb/12.0));


[nrow, ncol]=size(fQ);

header_cards = [make_card('SIMPLE','T');       ...
      make_card('BITPIX',16);       ...
      make_card('NAXIS',0);          ...
      make_card('EXTEND','T');        ...
      make_card('END');];
  
[nrowbis,ncolbis] = size(header_cards);
n_blanks = 36 - rem(nrowbis,36);
blank_line = setstr(ones(1,80)*32);
header_cards2 = [header_cards; repmat(blank_line,n_blanks,1)];

npix = 12*nside*nside;

header_cards2 = [header_cards2;       ...
      make_card('XTENSION','BINTABLE');        ...
      make_card('BITPIX',8);        ...
      make_card('NAXIS',2);          ...
      make_card('NAXIS1',16);      ...
      make_card('NAXIS2',ncol);      ...
      make_card('PCOUNT',0);        ...
      make_card('GCOUNT',1);        ...
      make_card('TFIELDS',2);        ...
      make_card('TTYPE1','Q_POLARISATION');        ...
      make_card('TFORM1','1D');        ...
      make_card('TUNIT1',' ');        ...
      make_card('TTYPE2','U_POLARISATION');        ...
      make_card('TFORM2','1D');        ...
      make_card('TUNIT2',' ');        ...
      make_card('EXTNAME','BINTABLE');        ...
      make_card('POLCCONV','COSMO');        ...
      make_card('PIXTYPE','HEALPIX');        ...
      make_card('ORDERING','RING');        ...
      make_card('NSIDE', nside);        ...
      make_card('NPIX', npix);        ...
      make_card('OBJECT', 'FULLSKY');        ...
      make_card('FIRTSPIX', 0);        ...
      make_card('LASTPIX', npix-1);        ...
      make_card('INDXSCHM', 'IMPLICIT');        ...
      make_card('BAD_DATA', -1.63750E+30);        ...
      make_card('END')];

header_record = make_header_record(header_cards2);
%[ncards,dummy]=size(header_cards);
%fprintf(header_record(1,:));

fid=fopen(filename,'w'); 
fwrite(fid,header_record','char');
fwrite(fid, [fQ; fU], 'double', 0, 'B');
fclose(fid);

function hrec=make_header_record(card_matrix)

[nrow,ncol] = size(card_matrix);
n_blanks = 36 - rem(nrow,36);
blank_line = setstr(ones(1,80)*32);
hrec = [card_matrix; repmat(blank_line,n_blanks,1)];
