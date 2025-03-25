"""
Robot klasa
===========

Opsta robot klasa koja prima osnovne informacije o robotu i vrsi mehanicke
proracuna
"""

"""
*** BIBLIOTEKE ***
"""
import numpy as np
from numpy.typing import NDArray
from typing import Optional, Sequence
from mehanika_robota import _alati
from mehanika_robota.mehanika import kinematika as kin
from mehanika_robota.mehanika import kretanje_krutog_tela as kkt

class Robot:
    def __init__(
        self,
        pocetna_konfig: Sequence | NDArray,
        ose_zavrtnja: Sequence | NDArray,
        opseg_aktuiranja: Sequence | NDArray | None = None,
        segmenti: Optional[
            Sequence | NDArray | int | float | np.int32 | np.float64
        ] = None,
        koord_sistem_prostor: bool = True,
        vek_kolona: bool = False
    ) -> None:
        
        self._pocetna_konfig = np.array(pocetna_konfig, dtype=float)
        _alati._mat_provera(self._pocetna_konfig, (4, 4), 'pocetna_konfig')
        
        self._ose_zavrtnja = np.array(ose_zavrtnja, dtype=float)
        
        # Klasa je napravljena da funkcionise sa matricom
        # `self._ose_zavrtnja`
        if self._ose_zavrtnja.ndim == 1:
            self._ose_zavrtnja = self._ose_zavrtnja[np.newaxis, :]
            
        # Za proracun sa smatra da je `self._ose_zavrtnja` matrica gde su ose
        # zavrtnja vektori kolone. Zato, ako je uneta `self._ose_zavrtnja` gde
        # su ose zavrtnja vektori reda, transponovati `self._ose_zavrtnja`
        if not vek_kolona:
            self._ose_zavrtnja = self._ose_zavrtnja.T
            
        # Proveri da li su vektori kolone `self._ose_zavrtnja` 6-dimenzionalni
        _alati._mat_provera(
            self._ose_zavrtnja,
            (6, self._ose_zavrtnja.shape[1]),
            "ose_zavrtnja"
        )
        
        # Normirati vektore ose zavrtnja
        self._ose_zavrtnja = np.apply_along_axis(
            kkt.v_prostor_normiranje, 0, self._ose_zavrtnja
        )
        
        # Radi jednostavnosti, klasa ce koristiti ose zavrtnja u prostornim
        # koordinatama
        if not koord_sistem_prostor:
            self._ose_zavrtnja = np.apply_along_axis(
                lambda osa_zavrtnja:
                    kkt.Ad(self._pocetna_konfig) @ osa_zavrtnja,
                0,
                self._ose_zavrtnja
            )
        
        if segmenti is not None:
            
            # Klasa koristi segmente u obliku 1D niza
            self._segmenti = np.atleast_1d(np.array(segmenti, dtype=float))

            if self._segmenti.ndim <= 2:
                if self._segmenti.ndim == 2 and self._segmenti.shape[1] > 1:
                    raise ValueError(
                        "Vektor \"segmenti\ mora biti dimenzije 1xn ili nx1"
                    )
            else:
                raise ValueError(
                    "Vektor \"segmenti\ mora biti dimenzije 1xn ili nx1"
                )
        else:
            self._segmenti = None
        
        if opseg_aktuiranja is not None:
            self._opseg_aktuiranja = np.array(opseg_aktuiranja, dtype=float)
            
            # Algoritam je napravljen da funkcionise sa matricom
            # `self._opseg_aktuiranja`
            if self._opseg_aktuiranja.ndim == 1:
                self._opseg_aktuiranja = self._opseg_aktuiranja[np.newaxis, :]
                
            # Matrica `self._opseg_aktuiranja` mora biti dimenzije nx2 gde je n
            # broj aktuatora, tj. broj kolona matrice `self._ose_zavrtnja`
            if not vek_kolona:
                self._opseg_aktuiranja = self._opseg_aktuiranja.T
            
            _alati._mat_provera(
                self._opseg_aktuiranja,
                (self.ose_zavrtnja.shape[1], 2),
                "ose_zavrtnja"
            )
            
            if np.any(
                self._opseg_aktuiranja[:, 0] >= self._opseg_aktuiranja[:, 1]
            ):
                raise ValueError(
                    "Nepravilan opseg aktuiranja. Donja granica aktuiranja "
                    "mora biti striktno manja od gornje za isti aktuator"
                )

        else:
            self._opseg_aktuiranja = None
            
    def _unutar_opsega_aktuiranja(self, pomeranja: Sequence | NDArray) -> bool:
        # Proverava da li su `pomeranja` unutar opsega aktuiranja
        if not np.all(tuple(
                # Donji prag aktuiranja i-tog aktuatora
                self._opseg_aktuiranja[i, 0]
                <= pomeranje
                # Donji prag aktuiranja i-tog aktuatora
                <= self._opseg_aktuiranja[i, 1]
                
                for i, pomeranje in enumerate(pomeranja)
        )):
            raise ValueError("Pomeranja iz \"pomeranja\" nisu unutar opsega aktuiranja")
    
    
    @property
    def pocetna_konfig(self) -> NDArray[np.float64]:
        return self._pocetna_konfig
    
    @property
    def ose_zavrtnja(self) -> NDArray[np.float64]:
        return self._ose_zavrtnja
    
    @property
    def opseg_aktuiranja(self) -> None | NDArray[np.float64]:
        return self._opseg_aktuiranja
    
    @property
    def segmenti(self) -> None | NDArray[np.float64]:
        return self._segmenti
    
    def dir_kin(
        self,
        pomeranja: Sequence | NDArray,
        koord_sistem_prostor: bool = True
    ) -> NDArray[np.float64]:
        if self._opseg_aktuiranja is not None:
            self._unutar_opsega_aktuiranja(pomeranja)

        if koord_sistem_prostor:
            return kin.dir_kin(
                self._pocetna_konfig,
                self._ose_zavrtnja,
                pomeranja,
                vek_kolona=True
            )
            
        else:
            return kkt.inv(kin.dir_kin(
                self._pocetna_konfig,
                self._ose_zavrtnja,
                pomeranja,
                vek_kolona=True
            ))
    
    #!def jakobijan(
    #     self,
    #     pomeranja: Optional[
    #         Sequence | NDArray | int | float | np.int32 | np.float64
    #     ] = None,
    #     koord_sistem_prostor: bool = True,
    #     vek_kolona: bool = False
    # ) -> NDArray[np.float64]:
    #
    #     if pomeranja is not None and self._opseg_aktuiranja is not None:
    #         self._unutar_opsega_aktuiranja(pomeranja)
        
    #!def manip
    #!def inv_kin