ALTER PROCEDURE [dbo].[GetMontoBPLAZA]
AS
BEGIN 
	SELECT VALOR
	FROM PARAMETROS
	WHERE ID =37
END

ALTER PROCEDURE [dbo].[GetMontoBVC]
AS
BEGIN 
	SELECT VALOR
	FROM PARAMETROS
	WHERE ID =34
END

ALTER PROCEDURE [dbo].[SP_consultaAfiliado720or722]
AS
BEGIN	
	SELECT afiCod FROM Afiliados where afiCod like '%720%' or afiCod like '%722%' 	
END

ALTER PROCEDURE [dbo].[SP_consultaHistoricoPago_p]
	@fecha date,
	@tipoConsulta int,
	@afiliado char(15)	
	
AS
BEGIN		
	IF	@tipoConsulta = 1
	
		SELECT 
			h.hisId,
			h.hisLote,
			h.hisRecordTDD,
			h.hisRecordTDC,
			h.hisAmountTDC,
			h.hisAmountTDCImpuesto,
			h.hisAmountIVA,
			h.hisAmountComisionBanco,
			h.hisAmountTotal,
			h.hisFechaEjecucion,
			h.hisFechaProceso,
			a.aboCodAfi,
			a.aboCodComercio,
			a.aboTerminal,
			a.aboCodBanco,
			a.aboNroCuenta,
			a.aboTipoCuenta,
			NULL as ref_bank,
			c.comerRif,
			c.comerDesc,
			c.comerTipoPer,
			c.comerPagaIva,
			c.comerCodUsuario,
			c.comerCodUsuario,
			c.comerCodPadre,
			cc.contNombres,
			cc.contApellidos,
			cc.contTelefLoc,
			cc.contTelefMov,
			cc.contMail,
			af.afiDesc,
			af.afiCodTipoPer
		FROM Historico h
		INNER JOIN Abonos a 
			ON h.aboCodAfi = a.aboCodAfi 
		and h.aboCodComercio = a.aboCodComercio 
		and h.aboTerminal = a.aboTerminal 
		INNER JOIN Comercios c 
			ON h.aboCodComercio = c.comerCod 
		LEFT JOIN Contactos cc 
			ON h.aboCodComercio = cc.contCodComer 
		LEFT JOIN Aliados al 
			ON al.id = c.comerCodAliado 
		INNER JOIN Afiliados af 
			ON h.aboCodAfi = af.afiCod 
		WHERE 
			convert(date ,h.hisFechaEjecucion) = @fecha 
			and h.hisAmountTotal > 0
			and h.aboCodAfi = @afiliado 
		ORDER BY a.aboCodComercio, h.hisId ASC
	
	ELSE IF @tipoConsulta = 2
	
		SELECT SUM(h.hisAmountTotal) as montoAbonoAliado ,al.id, al.aliTipoIdentificacion, al.aliIdentificacion, al.aliApellidos,
			al.aliNombres, al.aliEmail, al.aliDireccion, al.aliCodZonaAtencion, al.aliCodModalidadPago, al.aliCuentaAbono,
			al.aliCodEstatus   
		FROM Historico h INNER JOIN Comercios c ON h.aboCodComercio = c.comerCod INNER JOIN Abonos a ON h.aboCodAfi = a.aboCodAfi and h.aboCodComercio = a.aboCodComercio and h.aboTerminal = a.aboTerminal LEFT JOIN Contactos cc ON h.aboCodComercio = cc.contCodComer INNER JOIN Aliados al ON al.id = c.comerCodAliado INNER JOIN Afiliados af ON h.aboCodAfi = af.afiCod
		WHERE convert(date ,h.hisFechaEjecucion) = @fecha and h.aboCodAfi = @afiliado
		GROUP BY al.id, al.aliTipoIdentificacion, al.aliIdentificacion, al.aliApellidos,
			al.aliNombres, al.aliEmail, al.aliDireccion, al.aliCodZonaAtencion, al.aliCodModalidadPago, al.aliCuentaAbono,
			al.aliCodEstatus	

		IF	@tipoConsulta = 3
			SELECT 
				a.aboCodAfi,
				SUM(h.hisAmountTotal) AS TotalAmount,
				MAX(h.hisFechaProceso) AS UltimaFechaProceso,
				MAX(h.hisFechaEjecucion) AS UltimaFechaEjecucion
			FROM Historico h
			INNER JOIN Abonos a ON h.aboCodAfi = a.aboCodAfi AND h.aboTerminal = a.aboTerminal 
			WHERE 
				CONVERT(DATE, h.hisFechaEjecucion) = @fecha
				AND h.hisAmountTotal > 0
			GROUP BY a.aboCodAfi, h.hisFechaProceso, h.hisFechaEjecucion
END


ALTER  PROCEDURE [dbo].[SP_GetCuentaDebito]
	@afi char(3)
AS
BEGIN		
	IF	@afi = '720'
		SELECT valor FROM  parametros where id = 39
	ELSE IF @afi = '722'
		SELECT valor FROM  parametros where id = 40
END

ALTER PROCEDURE [dbo].[SP_GetTranredBangente]
AS
BEGIN 
	SELECT nro_cuenta, rif
	FROM cta_bank_pot
	WHERE ID =1
END