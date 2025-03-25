<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2"
    schemaVersion="ISO Schematron 2013">
  <pattern id="simple">
    <rule context="products">
      <assert test="product">The document root must contain a 'product' element.</assert>
    </rule>
  </pattern>
</schema>
