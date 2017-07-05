#!/usr/bin/env python

import hail
import json
from subprocess import call

hc = hail.HailContext(log = '/home/labbott/hail.log', parquet_compression = 'snappy')

(

	hc
	.import_vcf('gs://annotationdb/discovEHR/GHS_Freeze_50.L3DP10.pVCF.frq.vcf.bgz',)
	.annotate_variants_expr(
		"""
		va.AF = if (isDefined(va.info.AF))
			     va.info.AF[0]
		     else
		         0.001
		"""
	)
	.split_multi()
	.annotate_variants_expr('va = {AF: va.AF}')
	.write('gs://annotationdb/discovEHR/discovEHR.vds',overwrite = True)
)
